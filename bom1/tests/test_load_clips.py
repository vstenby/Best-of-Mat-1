import bom1 
import pytest
import pandas as pd

def test_load_clips():
    
    #Load clips will fail if there are any issues in the csv files.
    clips = bom1.load_clips()
    clips.columns == ['tag', 'nclip', 'name', 't1', 't2', 'rating', 'stream_title', 'link', 'duration']
    
    return

    