import bom1 
import pytest

def test_timestamp_to_seconds():
    
    s = bom1.timestamp_to_seconds('00:00:00.00')
    assert s == 0
    
    return