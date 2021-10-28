import bom1 
import pytest

def test_seconds_to_timestamp():
    
    ts = bom1.seconds_to_timestamp(0)
    assert ts == '00:00:00.00'

    return