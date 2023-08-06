#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
import pandas as pd

from ..transpile import transpile
from mitosheet.tests.test_utils import create_mito_wrapper, create_mito_wrapper_dfs


def test_transpile_single_column():
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, 'B', add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', 'df1[\'B\'] = df1[\'A\']']


def test_transpile_multiple_columns_no_relationship():
    mito = create_mito_wrapper(['abc'])
    mito.add_column(0, 'B')
    mito.add_column(0, 'C')
    code_container = transpile(mito.mito_widget.widget_state_container)
    
    assert len([line for line in code_container['code'] if 'df1[\'B\'] = 0' in line]) > 0
    assert len([line for line in code_container['code'] if 'df1[\'C\'] = 0' in line]) > 0

def test_transpile_columns_in_each_sheet():
    mito = create_mito_wrapper(['abc'], sheet_two_A_data=['abc'])
    mito.add_column(0, 'B')
    mito.add_column(1, 'B')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert len([line for line in code_container['code'] if 'df1[\'B\'] = 0' in line]) > 0
    assert len([line for line in code_container['code'] if 'df2[\'B\'] = 0' in line]) > 0

def test_transpile_multiple_columns_linear():
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, 'B', add_column=True)
    mito.set_formula('=B', 0, 'C', add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', 'df1[\'B\'] = df1[\'A\']', 'df1[\'C\'] = df1[\'B\']']

COLUMN_HEADERS = [
    ('ABC'),
    ('ABC_D'),
    ('ABC_DEF'),
    ('ABC_123'),
    ('ABC_HAHA_123'),
    ('ABC_HAHA-123'),
    ('---data---'),
    ('---da____ta---'),
    ('--'),
]
@pytest.mark.parametrize("column_header", COLUMN_HEADERS)
def test_transpile_column_headers_non_alphabet(column_header):
    mito = create_mito_wrapper(['abc'])
    mito.set_formula('=A', 0, column_header, add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', f'df1[\'{column_header}\'] = df1[\'A\']']


COLUMN_HEADERS = [
    ('ABC'),
    ('ABC_D'),
    ('ABC_DEF'),
    ('ABC_123'),
    ('ABC_HAHA_123'),
    ('ABC_HAHA-123'),
    ('---data---'),
    ('---da____ta---'),
    ('--'),
]
@pytest.mark.parametrize("column_header", COLUMN_HEADERS)
def test_transpile_column_headers_non_alphabet_multi_sheet(column_header):
    mito = create_mito_wrapper(['abc'], sheet_two_A_data=['abc'])
    mito.set_formula('=A', 0, column_header, add_column=True)
    mito.set_formula('=A', 1, column_header, add_column=True)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == ['# Step 1', f'df1[\'{column_header}\'] = df1[\'A\']', f'df2[\'{column_header}\'] = df2[\'A\']']

def test_preserves_order_columns():
    mito = create_mito_wrapper(['abc'])
    # Topological sort will currently display this in C, B order
    mito.add_column(0, 'B')
    mito.add_column(0, 'C')
    code_container = transpile(mito.mito_widget.widget_state_container)
    # Note: this optimizes out unnecessary code
    assert code_container['code'] == [
        '# Step 1', 
        '# Make sure the columns are defined in the correct order', 
        "df1['B'] = 0; df1['C'] = 0"
    ]

def test_transpile_merge_all_columns():
    df_one = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df_two = pd.DataFrame(data={'A': [1], 'D': [100], 'E': [10]})
    mito = create_mito_wrapper_dfs(df_one, df_two)

    mito.merge_sheets(0, 'A', list(df_one.keys()), 1, 'A', list(df_two.keys()))
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df3 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])'
    ]

def test_transpile_merge_some_all_columns():
    df_one = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df_two = pd.DataFrame(data={'A': [1], 'D': [100], 'E': [10]})
    mito = create_mito_wrapper_dfs(df_one, df_two)

    mito.merge_sheets(0, 'A', ['A', 'B'], 1, 'A', ['A', 'D'])
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        "temp_df = df2.drop_duplicates(subset='A')", 
        "df1_tmp = df1.drop(['C'], axis=1)", 
        "df2_tmp = temp_df.drop(['E'], axis=1)", 
        "df3 = df1_tmp.merge(df2_tmp, left_on=['A'], right_on=['A'], how='left', suffixes=['_df1', '_df2'])"
    ]

def test_transpile_merge_all_columns_than_some_columns():
    df_one = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df_two = pd.DataFrame(data={'A': [1], 'D': [100], 'E': [10]})
    mito = create_mito_wrapper_dfs(df_one, df_two)

    mito.merge_sheets(0, 'A', list(df_one.keys()), 1, 'A', list(df_two.keys()))    
    mito.merge_sheets(0, 'A', ['A', 'B'], 1, 'A', ['A', 'D'])

    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df3 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])',
        '# Step 2', 
        "temp_df = df2.drop_duplicates(subset='A')", 
        "df1_tmp = df1.drop(['C'], axis=1)", 
        "df2_tmp = temp_df.drop(['E'], axis=1)", 
        "df4 = df1_tmp.merge(df2_tmp, left_on=['A'], right_on=['A'], how='left', suffixes=['_df1', '_df2'])"
    ]

def test_transpile_delete_column():
    df1 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    mito = create_mito_wrapper_dfs(df1)
    mito.delete_column(0, 'C')

    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'df1.drop(\'C\', axis=1, inplace=True)'
    ]


# TESTING OPTIMIZATION

def test_removes_unedited_formulas_for_unedited_sheets():
    df1 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df2 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    mito = create_mito_wrapper_dfs(df1, df2)

    mito.set_formula('=C', 0, 'D', add_column=True)
    mito.set_formula('=C', 1, 'D', add_column=True)

    mito.merge_sheets(0, 'A', ['A', 'B', 'C', 'D'], 1, 'A', ['A', 'B', 'C', 'D'])

    mito.set_formula('=C + 1', 1, 'D', add_column=True)

    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'df1[\'D\'] = df1[\'C\']',
        'df2[\'D\'] = df2[\'C\']',
        '# Step 2', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df3 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])',
        '# Step 3', 
        'df2[\'D\'] = df2[\'C\'] + 1',
    ]


def test_mulitple_merges_no_formula_steps():
    df1 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df2 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    mito = create_mito_wrapper_dfs(df1, df2)
    mito.merge_sheets(0, 'A', ['A', 'B', 'C'], 1, 'A', ['A', 'B', 'C'])
    mito.merge_sheets(0, 'A', ['A', 'B', 'C'], 1, 'A', ['A', 'B', 'C'])
    mito.merge_sheets(0, 'A', ['A', 'B', 'C'], 1, 'A', ['A', 'B', 'C'])


    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df3 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])',
        '# Step 2', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df4 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])',
        '# Step 3', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df5 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])'
    ]

def test_optimization_with_other_edits():
    df1 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    df2 = pd.DataFrame(data={'A': [1], 'B': [101], 'C': [11]})
    mito = create_mito_wrapper_dfs(df1, df2)
    mito.set_formula('=A', 0, 'D', add_column=True)
    mito.merge_sheets(0, 'A', ['A', 'B', 'C', 'D'], 1, 'A', ['A', 'B', 'C'])
    mito.add_column(0, 'AAA')
    mito.delete_column(0, 'AAA')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1', 
        'df1[\'D\'] = df1[\'A\']',
        '# Step 2', 
        'temp_df = df2.drop_duplicates(subset=\'A\')', 
        'df3 = df1.merge(temp_df, left_on=[\'A\'], right_on=[\'A\'], how=\'left\', suffixes=[\'_df1\', \'_df2\'])',
        '# Step 3',
        'df1[\'AAA\'] = 0',
        'df1[\'D\'] = df1[\'A\']', # This line is included during a column add, because we just check if any formula has changed to include formulas for sheet
        '# Step 4', 
        'df1.drop(\'AAA\', axis=1, inplace=True)',
        '# Step 5',
        'df1[\'D\'] = df1[\'A\']', # This line is included during a column add, because we just check if any formula has changed to include formulas for sheet
    ]

def test_group_transpiles_single_columns():
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, ['Name'], {'Height': 'sum'}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"Name\"], as_index=False)',
        'df2 = groupby_obj.agg({\"Height\": \"sum\"})',
        'df2.rename(columns={\"Height\": \"sum_Height\"}, inplace=True)',
    ]

def test_group_transpiles_single_column_overlap_group_by_values():
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, ['Name'], {'Name': 'count'}
    )
    mito.group_sheet(
        0, ['Name'], {'Name': 'count'}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"Name\"], as_index=False)',
        'df2 = groupby_obj.size()',
        '# Step 2',
        'groupby_obj = df1.groupby([\"Name\"], as_index=False)',
        'df3 = groupby_obj.size()',
    ]

def test_group_leaves_early_with_no_agg_columns():
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, ['Name'], {}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"Name\"], as_index=False)',
        'df2 = groupby_obj.agg({})',
    ]

def test_group_transpiles_group_by_mulitple_columns():
    df1 = pd.DataFrame(data={'First_Name': ['Nate', 'Nate'], 'Last_Name': ['Rush', 'Jack'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, ['First_Name', 'Last_Name'], {'Height': 'sum'}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"First_Name\", \"Last_Name\"], as_index=False)',
        'df2 = groupby_obj.agg({\"Height\": \"sum\"})',
        'df2.rename(columns={\"Height\": \"sum_Height\"}, inplace=True)',
    ]

def test_group_transpiles_group_by_mulitple_columns_agg():
    df1 = pd.DataFrame(data={'First_Name': ['Nate', 'Nate'], 'Last_Name': ['Rush', 'Jack'], 'Height': [4, 5], 'Weight': [5, 6]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, ['First_Name', 'Last_Name'], {'Height': 'sum', 'Weight': 'mean'}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"First_Name\", \"Last_Name\"], as_index=False)',
        'df2 = groupby_obj.agg({\"Height\": \"sum\", \"Weight\": \"mean\"})',
        'df2.rename(columns={\"Height\": \"sum_Height\", \"Weight\": \"mean_Weight\"}, inplace=True)',
    ]

def test_group_transpiles_mulitple_sheets():
    df1 = pd.DataFrame(data={'First_Name': ['Nate', 'Nate'], 'Last_Name': ['Rush', 'Jack'], 'Height': [4, 5], 'Weight': [5, 6]})
    df2 = pd.DataFrame(data={'First_Name': ['Nate', 'Nate'], 'Last_Name': ['Rush', 'Jack'], 'Height': [4, 5], 'Weight': [5, 6]})
    mito = create_mito_wrapper_dfs(df1, df2)
    mito.group_sheet(
        0, ['First_Name', 'Last_Name'], {'Height': 'sum', 'Weight': 'mean'}
    )
    mito.group_sheet(
        1, ['First_Name', 'Last_Name'], {'Height': 'sum', 'Weight': 'mean'}
    )
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'groupby_obj = df1.groupby([\"First_Name\", \"Last_Name\"], as_index=False)',
        'df3 = groupby_obj.agg({\"Height\": \"sum\", \"Weight\": \"mean\"})',
        'df3.rename(columns={\"Height\": \"sum_Height\", \"Weight\": \"mean_Weight\"}, inplace=True)',
        '# Step 2',
        'groupby_obj = df2.groupby([\"First_Name\", \"Last_Name\"], as_index=False)',
        'df4 = groupby_obj.agg({\"Height\": \"sum\", \"Weight\": \"mean\"})',
        'df4.rename(columns={\"Height\": \"sum_Height\", \"Weight\": \"mean_Weight\"}, inplace=True)',
    ]


def test_transpile_initial_rename_mulitple_columns():
    df1 = pd.DataFrame(data={'First Name': ['Nate', 'Nate'], 'Last Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1 (rename headers to make them work with Mito)',
        'df1.rename(columns={\"First Name\": \"First_Name\", \"Last Name\": \"Last_Name\"}, inplace=True)',
    ]

def test_transpile_initial_rename_multiple_dfs():
    df1 = pd.DataFrame(data={'First Name': ['Nate', 'Nate'], 'Last_Name': ['Rush', 'Jack']})
    df2 = pd.DataFrame(data={'First_Name': ['Nate', 'Nate'], 'Last Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1, df2)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1 (rename headers to make them work with Mito)',
        'df1.rename(columns={\"First Name\": \"First_Name\"}, inplace=True)',
        'df2.rename(columns={\"Last Name\": \"Last_Name\"}, inplace=True)',
    ]

def test_transpile_filter():
    df1 = pd.DataFrame(data={'name': ['Nate', 'Jake'], 'Last_Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1)
    mito.filter(0, 'name', 'And', 'string', 'contains', 'Nate')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1 = df1[df1[\'name\'].str.contains(\'Nate\', na=False)]',
    ]

def test_transpile_date_filter():
    df = pd.DataFrame(data={'A': pd.to_datetime(pd.Series(data=[
        '12-2-2020', 
        '12-3-2020'
    ]))})
    mito = create_mito_wrapper_dfs(df)
    mito.filter(0, 'A', 'And', 'datetime', 'datetime_greater', '12-2-2020')
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1 = df1[df1[\'A\'] > pd.to_datetime(\'12-2-2020\')]',
    ]

def test_transpile_double_filter_and():
    df1 = pd.DataFrame(data={'name': ['Nate', 'Jake'], 'Last_Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1)
    mito.filters(0, 'name', 'And', [{'type': 'string', 'condition': 'contains', 'value': 'e'}, {'type': 'string', 'condition': 'string_exactly', 'value': 'Nate'}])
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1 = df1[(df1[\'name\'].str.contains(\'e\', na=False)) & (df1[\'name\'] == \'Nate\')]',
    ]

def test_transpile_double_filter_or():
    df1 = pd.DataFrame(data={'name': ['Nate', 'Jake'], 'Last_Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1)
    mito.filters(0, 'name', 'Or', [{'type': 'string', 'condition': 'contains', 'value': 'e'}, {'type': 'string', 'condition': 'string_exactly', 'value': 'Nate'}])
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1 = df1[(df1[\'name\'].str.contains(\'e\', na=False)) | (df1[\'name\'] == \'Nate\')]',
    ]

def test_transpile_triple_filter():
    df1 = pd.DataFrame(data={'name': ['Nate', 'Jake'], 'Last_Name': ['Rush', 'Jack']})
    mito = create_mito_wrapper_dfs(df1)
    mito.filters(0, 'name', 'Or', [{'type': 'string', 'condition': 'contains', 'value': 'e'}, {'type': 'string', 'condition': 'contains', 'value': 'a'}, {'type': 'string', 'condition': 'string_exactly', 'value': 'Nate'}])
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1 = df1[(df1[\'name\'].str.contains(\'e\', na=False)) | (df1[\'name\'].str.contains(\'a\', na=False)) | (df1[\'name\'] == \'Nate\')]',
    ]
    
def test_transpile_reorder_column():
    df1 = pd.DataFrame(data={'A': ['aaron'], 'B': ['jon']})
    mito = create_mito_wrapper_dfs(df1)
    mito.reorder_column(0, 'A', 1)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1_columns = [col for col in df1.columns if col != \'A\']',
        'df1_columns.insert(1, \'A\')',
        'df1 = df1[df1_columns]'
    ]

def test_transpile_two_column_reorders():
    df1 = pd.DataFrame(data={'A': ['aaron'], 'B': ['jon']})
    mito = create_mito_wrapper_dfs(df1)
    mito.reorder_column(0, 'A', 1)
    mito.reorder_column(0, 'B', 1)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1_columns = [col for col in df1.columns if col != \'A\']',
        'df1_columns.insert(1, \'A\')',
        'df1 = df1[df1_columns]',
        '# Step 2',
        'df1_columns = [col for col in df1.columns if col != \'B\']',
        'df1_columns.insert(1, \'B\')',
        'df1 = df1[df1_columns]'
    ]

def test_transpile_reorder_column_invalid():
    df1 = pd.DataFrame(data={'A': ['aaron'], 'B': ['jon']})
    mito = create_mito_wrapper_dfs(df1)
    mito.reorder_column(0, 'A', 5)
    code_container = transpile(mito.mito_widget.widget_state_container)
    assert code_container['code'] == [
        '# Step 1',
        'df1_columns = [col for col in df1.columns if col != \'A\']',
        'df1_columns.insert(1, \'A\')',
        'df1 = df1[df1_columns]',
    ]
