#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import uuid
from typing import Dict, Union, List
import pandas as pd
import numpy as np
import json
from copy import deepcopy, copy
from collections import OrderedDict

from mitosheet.steps import STEPS
from mitosheet.steps.initial_rename import execute_initial_rename_step
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.topological_sort import creates_circularity, topological_sort_columns
from mitosheet.parser import parse_formula, safe_replace
from mitosheet.utils import empty_column_python_code, dfs_to_json, is_valid_header, get_column_filter_type
from mitosheet.save_utils import write_analysis, read_analysis
from mitosheet.transpile import transpile
from mitosheet.errors import (
    make_no_sheet_error,
    make_column_exists_error,
    make_no_column_error,
    make_wrong_column_metatype_error,
    make_unsupported_function_error,
    make_circular_reference_error,
    make_execution_error,
    make_invalid_column_headers_error,
    make_invalid_column_delete_error,
    EditError
)


class WidgetStateContainer():
    """
    Holds all private widget state used by the evaluator and transpiler. 

    Is responsible for updating this state and maintaining correctness, 
    even in the case of invalid updates.

    Each state variable is a list where there is one entry for each
    dataframe passed to the WidgetStateContainer.
    """

    def __init__(self, dfs: pd.DataFrame):
        # just in case they are a tuple, make them a list - as it's easier to operate with...
        # and we make a copy so we don't modify the original dataframes!
        dfs = deepcopy(list(dfs))

        # We also save a copy of the initial dataframes, for easy access
        self.original_df_keys = [df.keys() for df in dfs]

        # The df_names are composed of two parts:
        # 1. The names of the variables passed into the mitosheet.sheet call (which don't change over time).
        # 2. The names of the dataframes that were created during the analysis (e.g. by a merge).
        # Until we get them from the frontend as an update_event, we default them to df1, df2, ...
        self.df_names = [f'df{i + 1}' for i in range(len(dfs))] 

        # For now, we just randomly generate analysis names. In the future, we'll let users
        # set their own analysis name! We append a UUID to note that this is not an analysis 
        # the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # We generate an initial rename step, which handles any issues with invalid headers
        # by converting them all to valid headers - which occurs before any formula step.
        dfs = execute_initial_rename_step(dfs)

        self.steps = [{
            'step_type': 'formula',
            # The column_metatype is if it stores formulas or values
            'column_metatype': [{key: 'value' for key in df.keys()} for df in dfs], 
            # The column_type is the type of the series in this column 
            'column_type': [{key: get_column_filter_type(df[key]) for key in df.keys()} for df in dfs],
            # We make column_spreadsheet_code an ordered dictonary to preserve the order the formulas
            # are inserted, which in turn makes sure when we save + rerun an analysis, it's recreated
            # in the correct order (and thus the column order is preserved).
            'column_spreadsheet_code': [OrderedDict({key: '' for key in df.keys()}) for df in dfs],
            # We also keep track of a list of the added columns in this step, so we can make
            # sure columns get defined in the correct order in the transpiled code
            'added_columns': [[] for df in dfs],
            'column_python_code': [{key: empty_column_python_code() for key in df.keys()} for df in dfs],
            'column_evaluation_graph': [{key: set() for key in df.keys()} for df in dfs],
            'column_filters': [{key: {'operator': 'And', 'filters': []} for key in df.keys()} for df in dfs],
            'dfs': dfs
        }]

    @property
    def df_names_json(self):
        return json.dumps({'df_names': self.df_names})

    @property
    def curr_step_id(self):
        return len(self.steps) - 1

    @property
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_id]

    @property
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_id]['dfs'])

    @property
    def dfs(self):
        return self.steps[self.curr_step_id]['dfs']

    @property
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 
        """
        return dfs_to_json(self.curr_step['dfs'])

    @property
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with the edit_event, and errors
        if the event is invalid. 
        """
        if edit_event['type'] == 'cell_edit':
            sheet_index = edit_event['sheet_index']
            column_header = edit_event['address']
            old_formula = edit_event['old_formula']
            new_formula = edit_event['new_formula']
            self.set_column_formula(sheet_index, column_header, old_formula, new_formula)
        elif edit_event['type'] == 'add_column':
            sheet_index = edit_event['sheet_index']
            column_header = edit_event['column_header']
            self.add_column(sheet_index, column_header)
        elif edit_event['type'] == 'column_header_edit':
            sheet_index = edit_event['sheet_index']
            old_column_header = edit_event['old_column_header']
            new_column_header = edit_event['new_column_header']
            self.rename_column(sheet_index, old_column_header, new_column_header)
        elif edit_event['type'] == 'column_delete':
            sheet_index = edit_event['sheet_index']
            column_header = edit_event['column_header']
            self.delete_column(sheet_index, column_header)
        elif edit_event['type'] == 'merge':
            # construct new data frame with merged data 
            self.merge_sheets(
                edit_event['sheet_index_one'],
                edit_event['merge_key_one'],
                edit_event['selected_columns_one'],
                edit_event['sheet_index_two'],
                edit_event['merge_key_two'],
                edit_event['selected_columns_two']
            )
        else:
            """
            The code below contains the _new_ step handling, where all steps as specified in a similar
            format and the can be looped over as such. 

            This code will eventually replace the code above which cases manually!
            """
            for new_step in STEPS:
                if edit_event['type'] == new_step['event_type']:
                    # Get the params for this event
                    params = {key: value for key, value in edit_event.items() if key in new_step['params']}
                    # Actually execute this event
                    new_step['execute'](self, **params)
                    # And then return
                    return

            # If we didn't find anything, then we error!
            raise Exception(f'{edit_event} is not an edit event!')

    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """

        if update_event['type'] == 'df_names_update':
            df_names = update_event['df_names']
            self.df_names = df_names
        elif update_event['type'] == 'save_analysis':
            analysis_name = update_event['analysis_name']
            write_analysis(self, analysis_name)
        elif update_event['type'] == 'use_existing_analysis_update':
            step_summaries = update_event['steps']
            self._rerun_analysis(step_summaries)
        else:
            raise Exception(f'{update_event} is not an update event!')

    def _rerun_analysis(self, step_summaries):
        """
        This function reapplies all the steps summarized in the passed step summaries, 
        which come from a saved analysis. 

        If any of the step summaries fails, this function tries to roll back to before
        it applied any of the stems
        """   
        # We make a shallow copy of the steps, as none of the objects
        # will be changed by the step summaries we apply   
        old_steps = copy(self.steps)  
        
        try:
            for step_id, step_summary in step_summaries.items():
                step_type = step_summary['step_type']

                if step_type == 'formula':
                    for sheet_index, column_spreadsheet_code in enumerate(step_summary['column_spreadsheet_code']):
                        for column_header, formula in column_spreadsheet_code.items():
                            # First, we make sure the columns all exist
                            if column_header not in self.dfs[sheet_index].keys():
                                self.add_column(sheet_index, column_header)

                            # Skip any column without a formula, as this is a data column!
                            if formula == '':
                                continue
                            
                            # And then we set all their formulas to the new values
                            self.set_column_formula(sheet_index, column_header, None, formula)

                elif step_type == 'merge':
                    self.merge_sheets(
                        step_summary['sheet_index_one'],
                        step_summary['merge_key_one'],
                        step_summary['selected_columns_one'],
                        step_summary['sheet_index_two'],
                        step_summary['merge_key_two'],
                        step_summary['selected_columns_two']
                    )
                elif step_type == 'column_rename':
                    sheet_index = step_summary['sheet_index']
                    old_column_header = step_summary['old_column_header']
                    new_column_header = step_summary['new_column_header']                
                    self.rename_column(sheet_index, old_column_header, new_column_header)
                elif step_type == 'column_delete':
                    self.delete_column(
                        step_summary['sheet_index'],
                        step_summary['column_header']
                    )
                else:
                    """
                    The code below contains the _new_ step handling, where all steps as specified in a similar
                    format and the can be looped over as such. 

                    This code will eventually replace the code above which cases manually!
                    """
                    found = False
                    for new_step in STEPS:
                        if step_type == new_step['step_type']:
                            found = True
                            # Get the params for this event
                            params = {key: value for key, value in step_summary.items() if key in new_step['params']}
                            # Actually execute this event
                            new_step['execute'](self, **params)
                    if not found:
                        raise Exception('Trying to recreate invalid step:', step_summary)

        except Exception as e:
            print(e)
            # We remove all applied steps if there was an error
            self.steps = old_steps

            # And report a generic error to the user
            raise make_execution_error()



    def _create_and_checkout_new_step(self, step_type):
        """
        Creates a new step with new_step_id and step_type that starts
        with the ending state of the previous step
        """
        new_step_id = self.curr_step_id + 1

        # the new step is a copy of the previous step, where we only take the data we need
        # (which is the formula content only)
        new_step = dict()

        new_step['step_type'] = step_type
        new_step['column_metatype'] = deepcopy(self.steps[new_step_id - 1]['column_metatype'])
        new_step['column_type'] = deepcopy(self.steps[new_step_id - 1]['column_type'])
        new_step['column_spreadsheet_code'] = deepcopy(self.steps[new_step_id - 1]['column_spreadsheet_code'])
        new_step['added_columns'] = [[] for df in self.steps[new_step_id - 1]['dfs']]
        new_step['column_python_code'] = deepcopy(self.steps[new_step_id - 1]['column_python_code'])
        new_step['column_evaluation_graph'] = deepcopy(self.steps[new_step_id - 1]['column_evaluation_graph'])
        new_step['column_filters'] = deepcopy(self.steps[new_step_id - 1]['column_filters'])
        new_step['dfs'] = deepcopy(self.steps[new_step_id - 1]['dfs'])

        # add the new step to list of steps
        self.steps.append(new_step)

    def _delete_curr_step(self):
        """
        Deletes the current step and rolls back a step!
        """
        self.steps.pop()

    def add_df_to_curr_step(self, new_df):
        """
        Helper function for adding a new dataframe to the current step!
        """
        # update dfs by appending new df
        self.curr_step['dfs'].append(new_df)
        # Also update the dataframe name
        self.df_names.append(f'df{len(self.df_names) + 1}')

        # Update all the variables that depend on column_headers
        column_headers = new_df.keys()
        self.curr_step['column_metatype'].append({column_header: 'value' for column_header in column_headers})
        self.curr_step['column_type'].append({column_header: get_column_filter_type(new_df[column_header]) for column_header in column_headers})
        self.curr_step['column_spreadsheet_code'].append({column_header: '' for column_header in column_headers})
        self.curr_step['column_python_code'].append({column_header: empty_column_python_code() for column_header in column_headers})
        self.curr_step['column_evaluation_graph'].append({column_header: set() for column_header in column_headers})
        self.curr_step['column_filters'].append({column_header: {'operator':'And', 'filters': []} for column_header in column_headers})


    def add_column(self, sheet_index: int, column_header: str):
        """
        Adds a column. Errors if the column already exists
        """
        if column_header in self.curr_step['column_metatype'][sheet_index]:
            raise make_column_exists_error(column_header)

        # Update the state variables
        self.curr_step['column_metatype'][sheet_index][column_header] = 'formula'
        self.curr_step['column_type'][sheet_index][column_header] = 'number'
        self.curr_step['column_spreadsheet_code'][sheet_index][column_header] = '=0'
        self.curr_step['column_python_code'][sheet_index][column_header] = empty_column_python_code()
        self.curr_step['column_python_code'][sheet_index][column_header]['column_formula_changes'] = f'df[\'{column_header}\'] = 0'
        self.curr_step['column_evaluation_graph'][sheet_index][column_header] = set()
        self.curr_step['column_filters'][sheet_index][column_header] = {'operator': 'And', 'filters': []}
        self.curr_step['added_columns'][sheet_index].append(column_header)

        # Update the dataframe; this cannot cause an error!
        self.curr_step['dfs'][sheet_index][column_header] = 0

    def delete_column(self, sheet_index: int, column_header: str):
        """
        Creates a new step that deletes a the column column_heder 
        from the sheet at sheet_index.
        """
        # Error if the column does not exist
        if column_header not in self.curr_step['column_metatype'][sheet_index]:
            raise make_no_column_error([column_header])
        
        # Error if there are any columns that currently rely on this column
        if len(self.curr_step['column_evaluation_graph'][sheet_index][column_header]) > 0:
            raise make_invalid_column_delete_error(
                column_header,
                list(self.curr_step['column_evaluation_graph'][sheet_index][column_header])
            )

        # Make a new step for the delete
        self._create_and_checkout_new_step('column_delete')

        # Actually drop the column, and as we check for all possible errors above, 
        # we do not need to try this on a df copy first.
        df = self.curr_step['dfs'][sheet_index]
        df.drop(column_header, axis=1, inplace=True)

        # And then update all the state variables removing this column from the state
        del self.curr_step['column_metatype'][sheet_index][column_header]
        del self.curr_step['column_type'][sheet_index][column_header]
        del self.curr_step['column_spreadsheet_code'][sheet_index][column_header]
        del self.curr_step['column_python_code'][sheet_index][column_header]
        del self.curr_step['column_evaluation_graph'][sheet_index][column_header]
        # We also have to delete the places in the graph where this node is 
        for dependents in self.curr_step['column_evaluation_graph'][sheet_index].values():
            if column_header in dependents:
                dependents.remove(column_header)

        # And save code to do this
        df_name = self.df_names[sheet_index]
        self.curr_step['delete_code'] = [f'{df_name}.drop(\'{column_header}\', axis=1, inplace=True)']

        # Save data for analysis
        self.curr_step['sheet_index'] = sheet_index
        self.curr_step['column_header'] = column_header

        # Make a new column
        self._create_and_checkout_new_step('formula')


    def rename_column(self, sheet_index: int, old_column_header: str, new_column_header: str):
        """
        Renames the column from df at sheet_index from old_column_header to new_column.

        Creates two new steps to do this: 
        1. A column_rename step.
        2. A formula step after this column_rename step.

        In the step after the formula step, works to update all refrences to the old
        column throughout the step, including other formulas and the column
        evaluation graph.
        """
        if not is_valid_header(new_column_header):
            raise make_invalid_column_headers_error([new_column_header])

        if new_column_header in self.curr_step['dfs'][sheet_index].keys():
            raise make_column_exists_error(new_column_header)

        self._create_and_checkout_new_step('column_rename')

        # Execute the rename
        self.curr_step['dfs'][sheet_index].rename(columns={old_column_header: new_column_header}, inplace=True)

        # Save all the rename data
        df_name = self.df_names[sheet_index]
        rename_dict = "{\"" + old_column_header + "\": \"" + new_column_header + "\"}"
        self.curr_step['rename_code'] = [f'{df_name}.rename(columns={rename_dict}, inplace=True)']
        self.curr_step['sheet_index'] = sheet_index
        self.curr_step['old_column_header'] = old_column_header
        self.curr_step['new_column_header'] = new_column_header

        # Then, we update the current step to be valid, namely by deleting the old column (wherever it is)
        # and replacing it with the new column. 
        sheet_column_metatype = self.curr_step['column_metatype'][sheet_index]
        sheet_column_metatype[new_column_header] = sheet_column_metatype[old_column_header]

        sheet_column_type = self.curr_step['column_type'][sheet_index]
        sheet_column_type[new_column_header] = sheet_column_type[old_column_header]

        sheet_column_spreadsheet_code = self.curr_step['column_spreadsheet_code'][sheet_index]
        sheet_column_spreadsheet_code[new_column_header] = sheet_column_spreadsheet_code[old_column_header]

        sheet_column_python_code = self.curr_step['column_python_code'][sheet_index]
        sheet_column_python_code[new_column_header] = empty_column_python_code()
        
        sheet_column_evaluation_graph = self.curr_step['column_evaluation_graph'][sheet_index]
        sheet_column_evaluation_graph[new_column_header] = sheet_column_evaluation_graph[old_column_header]

        sheet_column_filters = self.curr_step['column_filters'][sheet_index]
        sheet_column_filters[new_column_header] = sheet_column_filters[old_column_header]

        # We also have to go over _all_ the formulas in the sheet that reference this column, and update
        # their references to the new column. 
        for column_header in sheet_column_evaluation_graph[new_column_header]:
            old_formula = sheet_column_spreadsheet_code[column_header]
            new_formula = safe_replace(
                old_formula,
                old_column_header,
                new_column_header
            )

            # NOTE: this only update the columns that rely on the renamed columns - it does
            # not update the columns that the renamed column on. We handle that below!
            self.set_column_formula(
                sheet_index,
                column_header,
                old_formula,
                new_formula
            )
        # We then have to go through and update the evaluation graphs
        # for the columns the renamed column relied on.
        for dependents in sheet_column_evaluation_graph.values():
            if old_column_header in dependents:
                dependents.remove(old_column_header)
                dependents.add(new_column_header)

        # We delete all references to the old_column header
        # NOTE: this has to happen after the above formula setting, so that
        # the dependencies can be updated properly!
        del sheet_column_metatype[old_column_header]
        del sheet_column_type[old_column_header]
        del sheet_column_spreadsheet_code[old_column_header]
        del sheet_column_python_code[old_column_header]
        del sheet_column_evaluation_graph[old_column_header]
        del sheet_column_filters[old_column_header]

        # Finially, we go back to a formula step - which should now be valid with all
        # the changes above!
        self._create_and_checkout_new_step('formula')


    def set_column_formula(
            self, 
            sheet_index: int,
            column_header: str, 
            old_formula: Union[str, None], 
            new_formula: str
        ):
        """
        Sets the column with column_header to have the new_formula, and 
        updates the dataframe as a result.

        Errors if:
        - The given column_header is not a column. 
        - The new_formula introduces a circular reference.
        - The new_formula causes an execution error in any way. 

        In the case of an error, this function rolls back all variables
        variables to their state at the start of this function.
        """

        # TODO: we need to make a column does not exist error, for this edit!

        # First, we check the column_metatype, and make sure it's a formula
        if self.curr_step['column_metatype'][sheet_index][column_header] != 'formula':
            raise make_wrong_column_metatype_error(column_header)

        # If nothings changed, there's no work to do
        if (old_formula == new_formula):
            return

        # Then we try and parse the formula
        new_python_code, new_functions, new_dependencies = parse_formula(
            new_formula, 
            column_header
        )

        # We check that the formula doesn't reference any columns that don't exist
        missing_columns = new_dependencies.difference(self.curr_step['column_metatype'][sheet_index].keys())
        if any(missing_columns):
            raise make_no_column_error(missing_columns)

        # The formula can only reference known formulas
        missing_functions = new_functions.difference(set(FUNCTIONS.keys()))
        if any(missing_functions):
            raise make_unsupported_function_error(missing_functions)

        # Then, we get the list of old column dependencies and new dependencies
        # so that we can update the graph
        old_python_code, old_functions, old_dependencies = parse_formula(old_formula, column_header)

        # Before changing any variables, we make sure this edit didn't
        # introduct any circularity
        circularity = creates_circularity(
            self.curr_step['column_evaluation_graph'][sheet_index], 
            column_header,
            old_dependencies,
            new_dependencies
        )
        if circularity:
            raise make_circular_reference_error()

        # Update the variables based on this new formula
        self.curr_step['column_spreadsheet_code'][sheet_index][column_header] = new_formula
        self.curr_step['column_python_code'][sheet_index][column_header]['column_formula_changes'] = new_python_code

        # Update the column dependency graph
        for old_dependency in old_dependencies:
            self.curr_step['column_evaluation_graph'][sheet_index][old_dependency].remove(column_header)
        for new_dependency in new_dependencies:
            self.curr_step['column_evaluation_graph'][sheet_index][new_dependency].add(column_header)

        # Then we update the dataframe, first by executing on a fake dataframe
        try:
            df_copy = self.curr_step['dfs'][sheet_index].copy()
            # We execute on the copy first to see if there will be errors
            self._execute(df_copy, sheet_index)
        except Exception as e:
            # If there is an error during executing, we roll back all the changes we made
            self.curr_step['column_spreadsheet_code'][sheet_index][column_header] = old_formula
            self.curr_step['column_python_code'][sheet_index][column_header]['column_formula_changes'] = old_python_code

            # Update the column dependency graph back to what it was.
            for new_dependency in new_dependencies:
                self.curr_step['column_evaluation_graph'][sheet_index][new_dependency].remove(column_header)
            for old_dependency in old_dependencies:
                self.curr_step['column_evaluation_graph'][sheet_index][old_dependency].add(column_header)
            
            # And then we bubble the error up!
            if isinstance(e, EditError):
                # If it's an edit error, we propagate that up
                raise e
            else:
                # Otherwise, we turn it into an edit error!
                raise make_execution_error()
            
        # However, if there was no error in execution on the copy, we can execute on 
        # the real dataframe!
        self._execute(self.curr_step['dfs'][sheet_index], sheet_index)

        # Finially, update the type of the filters of this column, for all the filters
        new_type = get_column_filter_type(self.curr_step['dfs'][sheet_index][column_header])
        self.curr_step['column_type'][sheet_index][column_header] = new_type
        self.curr_step['column_filters'][sheet_index][column_header]['filters'] = [
            {'type': new_type, 'condition': filter_['condition'], 'value': filter_['value']} 
            for filter_ in self.curr_step['column_filters'][sheet_index][column_header]['filters']
        ]

    def merge_sheets(
            self,
            sheet_index_one: int,
            merge_key_one: str,
            selected_columns_one,
            sheet_index_two: int,
            merge_key_two: str,
            selected_columns_two
        ):
        """
        Creates a new sheet by merging sheet_index_one and sheet_index_two together
        on the keys merge_key_one and merge_key_two respectively. 
        
        Note, that merge does not treat np.NaN = np.NaN, so NaN keys won't be matched 
        with anything, making any column in the second sheet NaN for that row in the resulting merged sheet.
        
        The merged sheet will contain all of the columns from sheet_index_one 
        and sheet_index_two

        If either merge key does not exist, it raises an exception.
        """
        # if the sheets don't exist, throw an error
        if not self.does_sheet_index_exist(sheet_index_one):
            raise make_no_sheet_error(sheet_index_one)

        if not self.does_sheet_index_exist(sheet_index_two):
            raise make_no_sheet_error(sheet_index_two)

        # We check that the merge doesn't use any columns that don't exist
        # TODO: update make_no_columns_error to use sheet names also
        missing_sheet_one_key = {merge_key_one}.difference(self.curr_step['column_metatype'][sheet_index_one].keys())
        if any(missing_sheet_one_key):
            raise make_no_column_error(missing_sheet_one_key)

        missing_sheet_two_key = {merge_key_two}.difference(self.curr_step['column_metatype'][sheet_index_two].keys())
        if any(missing_sheet_two_key):
            raise make_no_column_error(missing_sheet_two_key)

        # If no errors we create a new step for this merge
        self._create_and_checkout_new_step('merge')

        # Then we update the dataframe, first by executing on a fake dataframe
        try:    
            # make a copy of our data frame to test operate on 
            dfs_copy = deepcopy(self.curr_step['dfs'])

            # We execute on the copy first to see if there will be errors
            self._execute_merge(
                dfs_copy, 
                sheet_index_one,
                merge_key_one,
                selected_columns_one,
                sheet_index_two,
                merge_key_two,
                selected_columns_two
            )
        except EditError as e:
            # If an edit error occurs, we delete the merge step
            self._delete_curr_step()
            # And we propagate this error upwards
            raise e
        except Exception as e:
            print(e)
            # If any other error occurs, we delete the merge step
            self._delete_curr_step()
            # We raise a generic execution error in this case!
            raise make_execution_error()

        # if there was no error in execution on the copy, execute on real dataframes
        new_df = self._execute_merge(
                    self.curr_step['dfs'], 
                    sheet_index_one,
                    merge_key_one,
                    selected_columns_one,
                    sheet_index_two,
                    merge_key_two,
                    selected_columns_two
                )    

        # Add this dataframe to the current step!
        self.add_df_to_curr_step(new_df)

        # update df indexes to start at 1
        df_one_name = self.df_names[sheet_index_one]
        df_two_name = self.df_names[sheet_index_two]
        df_new_name = self.df_names[len(self.df_names) - 1]

        # Now, we build the merge code (starting with the code for dropping duplicates)
        merge_code = [
            f'temp_df = {df_two_name}.drop_duplicates(subset=\'{merge_key_two}\')',
        ]

        # If we are only taking some columns, write the code to drop the ones we don't need!
        deleted_columns_one = set(self.curr_step['dfs'][sheet_index_one].keys()).difference(set(selected_columns_one))
        deleted_columns_two = set(self.curr_step['dfs'][sheet_index_two].keys()).difference(set(selected_columns_two))
        if len(deleted_columns_one) > 0:
            merge_code.append(
                f'{df_one_name}_tmp = {df_one_name}.drop({list(deleted_columns_one)}, axis=1)'
            )
        if len(deleted_columns_two) > 0:
            merge_code.append(
                f'{df_two_name}_tmp = temp_df.drop({list(deleted_columns_two)}, axis=1)'
            )

        # If we drop columns, we merge the new dataframes
        df_one_to_merge = df_one_name if len(deleted_columns_one) == 0 else f'{df_one_name}_tmp'
        df_two_to_merge = 'temp_df' if len(deleted_columns_two) == 0 else f'{df_two_name}_tmp'

        # Finially append the merge
        merge_code.append(
            f'{df_new_name} = {df_one_to_merge}.merge({df_two_to_merge}, left_on=[\'{merge_key_one}\'], right_on=[\'{merge_key_two}\'], how=\'left\', suffixes=[\'_{df_one_name}\', \'_{df_two_name}\'])'
        )

        # And then save it
        self.curr_step['merge_code'] = merge_code

        # update the step to save the variables needed to reconstruct the merge
        self.curr_step['sheet_index_one'] = sheet_index_one
        self.curr_step['sheet_index_two'] = sheet_index_two
        self.curr_step['merge_key_one'] = merge_key_one
        self.curr_step['merge_key_two'] = merge_key_two
        self.curr_step['selected_columns_one'] = selected_columns_one
        self.curr_step['selected_columns_two'] = selected_columns_two

        # after done merging, we create and checkout a new formula step!
        self._create_and_checkout_new_step('formula')

    def does_sheet_index_exist(self, index):
        return not (index < 0 or index >= self.num_sheets)
    

    def _execute(self, df, sheet_index):
        """
        Executes the given state variables for  
        """

        topological_sort = topological_sort_columns(self.curr_step['column_evaluation_graph'][sheet_index])

        for column_header in topological_sort:
            # Exec the code, where the df is the original dataframe
            # See explination here: https://www.tutorialspoint.com/exec-in-python
            exec(
                self.curr_step['column_python_code'][sheet_index][column_header]['column_formula_changes'],
                {'df': df}, 
                FUNCTIONS
            )
        
    def _execute_merge(
            self, 
            dfs, 
            sheet_index_one,
            merge_key_one, 
            selected_columns_one,
            sheet_index_two,
            merge_key_two,
            selected_columns_two
        ):
        """
        Executes a merge on the sheets with the given indexes, merging on the 
        given keys, and only keeping the selection columns from each df.
        
        TODO: figure out how to simulate VLOOKUP style work better here...
        """
        # We drop duplicates to avoid pairwise duplication on the merge.
        temp_df = dfs[sheet_index_two].drop_duplicates(subset=merge_key_two)

        # Then we delete all the columns from each we don't wanna keep
        deleted_columns_one = set(dfs[sheet_index_one].keys()).difference(set(selected_columns_one))
        deleted_columns_two = set(dfs[sheet_index_two].keys()).difference(set(selected_columns_two))

        df_one_cleaned = dfs[sheet_index_one].drop(deleted_columns_one, axis=1)
        df_two_cleaned = temp_df.drop(deleted_columns_two, axis=1)

        # Finially, we perform the merge!
        df_one_name = self.df_names[sheet_index_one]
        df_two_name = self.df_names[sheet_index_two]
        return df_one_cleaned.merge(df_two_cleaned, left_on=[merge_key_one], right_on=[merge_key_two], how='left', suffixes=[f'_{df_one_name}', f'_{df_two_name}'])