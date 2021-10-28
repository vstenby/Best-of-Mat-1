#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .load_clips import load_clips
import pandas as pd
import numpy as np

def test_load_scripts():
    '''
    This should be able to catch most errors in all of the lecture clipping csvs.
    '''
    clips = load_clips()
    columns = clips.columns
    
    expected_columns = ['tag', 'nclip', 'name', 't1', 't2', 'rating', 'stream_title', 'link', 'duration']
    
    for expected_column in expected_columns:
        assert expected_column in columns, f'Column {expected_column} was expected but not found in dataframe returned from load_clips().'    
    
    for column in columns:
        assert column in expected_columns, f'Column {column} was returned by load_clips() but was unexpected.'
        
    return
        
def test_metadata():
    '''
    This catches errors in the metadata csv file.
    '''
    df = pd.isna(pd.read_csv('./csv/metadata.csv'))
    assert ~np.any(df), 'metadata should be filled in. Use the fill_metadata() function!'
    assert np.all(df.columns == ['tag', 'stream_title', 'link'])
    return