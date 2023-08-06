#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A group step, which allows you to group data
from an existing dataframe along some keys, and then
aggregate other columns with specific functions.
"""
import json
from copy import deepcopy
from pandas.core.base import DataError

from mitosheet.utils import get_column_filter_type
from mitosheet.errors import (
    EditError,
    make_no_sheet_error,
    make_no_column_error,
    make_execution_error,
    make_invalid_aggregation_error
)

GROUP_BY_EVENT = 'group_edit'
GROUP_BY_STEP_TYPE = 'group'

GROUP_BY_PARAMS = [
    'sheet_index', # int
    'group_by_keys', # list of column_headers (at least of length 1)
    'values', # a dict from column_header -> aggregation function
]

def execute_group_step(
        wsc,
        sheet_index,
        group_by_keys,
        values
    ):
    """
    The function responsible for updating the widget state container
    with a new group step.

    If it fails part of the way through, deletes the new group step entirely.
    """

    # if the sheets don't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the group by doesn't use any columns that don't exist
    missing_group_by_keys = set(group_by_keys).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_group_by_keys) > 0:
        raise make_no_column_error(missing_group_by_keys)

    missing_value_keys = set(values.keys()).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_value_keys) > 0:
        raise make_no_column_error(missing_value_keys)

    # Create a new step
    wsc._create_and_checkout_new_step(GROUP_BY_STEP_TYPE)

    # Save the params of the current step
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['group_by_keys'] = group_by_keys
    wsc.curr_step['values'] = values

    try:
        # TODO: this speculative execution, once we have all the steps
        # standardized (and only appending on the end), can be moved
        # out of these functions! We just need to delete the new step
        _execute_group(
            deepcopy(wsc.curr_step['dfs'][sheet_index]), 
            group_by_keys,
            values
        )
    except EditError as e:
        print(e)
        # If an edit error occurs, we delete the group step
        wsc._delete_curr_step()
        # And we propagate this error upwards
        raise e
    except DataError as e:
        # A data-error occurs when you try to aggregate on a column where the function
        # cannot be applied (e.g. 'mean' on a column of strings)
        print(e)
        # Delete the current step
        wsc._delete_curr_step()
        # Generate an error informing the user
        raise make_invalid_aggregation_error()

    except Exception as e:
        print(e)
        # If any other error occurs, we delete the group step
        wsc._delete_curr_step()
        # We raise a generic execution error in this case!
        raise make_execution_error()

    # Actually execute the grouping
    new_df = _execute_group(
        wsc.curr_step['dfs'][sheet_index],
        group_by_keys,
        values
    )

    # Add it to the dataframe
    wsc.add_df_to_curr_step(new_df)

    # And finially move back to a formula step
    wsc._create_and_checkout_new_step('formula')


def _execute_group(df, group_by_keys, values):
    """
    Helper function for executing the groupby on a specific dataframe
    and then aggregating the values with the passed values mapping
    """
    groupby_obj = df.groupby(group_by_keys, as_index=False)

    # We have a special case for when the user has grouped by the key
    # that they also want to count (Brian Mathis has this!), where we 
    # calculate the size instead of a standard aggregation (which appears
    # to not support overlapping group_by_keys and values to aggregate.)
    if len(group_by_keys) == 1 and {group_by_keys[0]: 'count'} == values:
        return groupby_obj.size()

    agged_df = groupby_obj.agg(values)
    new_names = {
        key: f'{value + "_" + key}' for key, value in values.items()
    }
    agged_df.rename(columns=new_names, inplace=True)
    return agged_df


def transpile_group_step(
        widget_state_container,
        new_df_name,
        sheet_index,
        group_by_keys,
        values
    ):
    """
    Transpiles a group step to python code!

    TODO: new_df_name is a workaround while we figure out where / when this transpile code
    gets called. As it may not be called when the group step being transpiled is the current
    step in the widget state container, we do not know what the name of the new dataframe
    we create should be. 
    
    Another potential way to handle this is to saturate the event with this data when it comes
    to the backend, which seems reasonable, I think...
    """
    # Group
    group_line = f'groupby_obj = {widget_state_container.df_names[sheet_index]}.groupby({json.dumps(group_by_keys)}, as_index=False)'
    # Aggregate

    # We have a special case for when the user has grouped by the key
    # that they also want to count (Brian Mathis has this!), where we 
    # calculate the size instead of a standard aggregation (which appears
    # to not support overlapping group_by_keys and values to aggregate.)
    if len(group_by_keys) == 1 and {group_by_keys[0]: 'count'} == values:
        size_line = f'{new_df_name} = groupby_obj.size()'
        return [group_line, size_line]

    agg_line = f'{new_df_name} = groupby_obj.agg({json.dumps(values)})'
    # We short circuit if there is no values to keep, and so nothing to really aggregate by (or rename)
    # NOTE: we still need the agg line, as the groupby_obj is not a dataframe!
    if len(values) == 0:
        return [group_line, agg_line]

    # Rename (first construct the map)
    new_names = {
        key: f'{value + "_" + key}' for key, value in values.items()
    }
    rename_line = f'{new_df_name}.rename(columns={json.dumps(new_names)}, inplace=True)'

    return [group_line, agg_line, rename_line]

"""
This object wraps all the information
that is needed for a group-by step!
"""
GROUP_BY_STEP = {
    'event_type': GROUP_BY_EVENT,
    'step_type': GROUP_BY_STEP_TYPE,
    'params': GROUP_BY_PARAMS,
    'execute': execute_group_step,
    'transpile': transpile_group_step
}





