#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bom1 import *
import pandas as pd
import numpy as np

def test_load_scripts():
    
    clips = load_clips()
    columns = clips.columns
    
    expected_columns = ['tag', 'nclip', 'name', 't1', 't2', 'rating', 'stream_title', 'link', 'stream_link', 'download_link', 'duration']
    
    for expected_column in expected_columns:
        assert expected_column in columns, f'Column {expected_column} was expected but not found in dataframe returned from load_clips().'    
    
    for column in columns:
        assert column in expected_columns, f'Column {column} was returned by load_clips() but was unexpected.'