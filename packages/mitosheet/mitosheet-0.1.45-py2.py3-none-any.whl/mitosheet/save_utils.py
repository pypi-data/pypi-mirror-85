#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions for saving and reading
in analyses.
"""

import os
import json
import pandas as pd
from string import ascii_letters, digits

from mitosheet._version import __version__
from mitosheet.steps import STEPS

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The current version of the saved Mito analysis
# where we save all the analyses for this version
CURRENT_VERSION_MITO_FOLDER = os.path.join(MITO_FOLDER, __version__)


def read_analysis(analysis_name):
    """
    Given an analysis_name, reads the saved analysis in
    ~/.mito/{analysis_name}.json and returns a JSON object
    representing it.
    """
    analysis_path = f'{CURRENT_VERSION_MITO_FOLDER}/{analysis_name}.json'

    if not os.path.exists(analysis_path):
        return None

    with open(analysis_path) as f:
        try:
            # We try and read the file as JSON
            return json.load(f)
        except: 
            return None

def _get_all_analysis_filenames():
    """
    Returns the names of the files in the CURRENT_VERSION_MITO_FOLDER
    """
    if not os.path.exists(CURRENT_VERSION_MITO_FOLDER):
        return []

    file_names = set([
        f for f in os.listdir(CURRENT_VERSION_MITO_FOLDER) 
        if os.path.isfile(os.path.join(CURRENT_VERSION_MITO_FOLDER, f))
    ])

    return file_names

def _delete_analyses(analysis_filenames):
    """
    For bulk deleting analysis with file names. 
    """
    for filename in analysis_filenames:
        os.remove(os.path.join(CURRENT_VERSION_MITO_FOLDER, filename))

def read_saved_analysis_names():
    """
    Reads the names of all the analyses saved by the user.

    Does not return any of the auto-saved analyses!
    """
    if not os.path.exists(CURRENT_VERSION_MITO_FOLDER):
        return []

    file_names = [
        f for f in os.listdir(CURRENT_VERSION_MITO_FOLDER) 
        if os.path.isfile(os.path.join(CURRENT_VERSION_MITO_FOLDER, f))
        and not f.startswith('UUID-')
    ]

    # We make sure they are in alphabetical order!
    file_names.sort()

    return [
        file_name[:-5] for file_name in file_names 
        if file_name.endswith('.json')
    ]

def saved_analysis_names_json():
    return json.dumps(read_saved_analysis_names())

def make_steps_json_obj(steps):
    """
    Given a steps dictonary from a widget_state_container, puts the steps
    into a format that can be saved and recreated. Necessary for saving an
    analysis to a file!
    """
    steps_json_obj = dict()
    for step_id, step in enumerate(steps):
        step_type = step['step_type']
        if step_type == 'formula':
            steps_json_obj[step_id] = {
                'step_type': step_type,
                'column_spreadsheet_code': step['column_spreadsheet_code']
            }
        elif step_type == 'merge':
            steps_json_obj[step_id] = {
                'step_type': step_type,
                'sheet_index_one': step['sheet_index_one'],
                'selected_columns_one': step['selected_columns_one'],
                'merge_key_one': step['merge_key_one'],
                'sheet_index_two': step['sheet_index_two'],
                'merge_key_two': step['merge_key_two'],
                'selected_columns_two': step['selected_columns_two']
            }
        elif step_type == 'column_rename':
            steps_json_obj[step_id] = {
                'step_type': 'column_rename',
                'sheet_index': step['sheet_index'],
                'old_column_header': step['old_column_header'],
                'new_column_header': step['new_column_header']
            }
        elif step_type == 'column_delete':
            steps_json_obj[step_id] = {
                'step_type': 'column_delete',
                'sheet_index': step['sheet_index'],
                'column_header': step['column_header']
            }
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

                    # Save the step type
                    step_summary = {
                        'step_type': step_type
                    }
                    # As all as all the parameters!
                    step_summary.update({key: value for key, value in step.items() if key in new_step['params']})

                    steps_json_obj[step_id] = step_summary

            if not found:
                raise Exception("make sure all steps are defined in make_steps_json_obj")

    return steps_json_obj


def write_analysis(widget_state_container, analysis_name=None):
    """
    Writes the analysis saved in widget_state_container to
    ~/.mito/{analysis_name}. If analysis_name is none, gets the temporary
    name from the widget_state_container.

    NOTE: as the written analysis is from the widget_state_container,
    we assume that the analysis is valid when written and read back in!
    """

    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    if not os.path.exists(CURRENT_VERSION_MITO_FOLDER):
        os.mkdir(CURRENT_VERSION_MITO_FOLDER)

    if analysis_name is None:
        analysis_name = widget_state_container.analysis_name

    analysis_path = f'{CURRENT_VERSION_MITO_FOLDER}/{analysis_name}.json'

    with open(analysis_path, 'w+') as f:
        steps_json_obj = make_steps_json_obj(widget_state_container.steps)

        f.write(json.dumps({
            'steps': steps_json_obj
        }))
