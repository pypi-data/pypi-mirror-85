#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
See mito/mitosheet/steps/README.md for more information about 
how to add a step!

NOTE: this new step refactor is a WIP, and will not be finished
until we remove all the manual step casing that occurs throughout the 
codebase. This is an incremental process that will take time!
"""

from mitosheet.steps.group import GROUP_BY_STEP
from mitosheet.steps.filter import FILTER_STEP
from mitosheet.steps.reorder_column import REORDER_COLUMN_STEP


# All steps must be listed in this variable.
STEPS = [
    GROUP_BY_STEP,
    REORDER_COLUMN_STEP,
    FILTER_STEP
]