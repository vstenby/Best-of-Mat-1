from .seconds_to_timestamp import *
from .timestamp_to_seconds import *

def duration(t1, t2):
    t1  = timestamp_to_seconds(t1)
    t2  = timestamp_to_seconds(t2)
    dur = t2-t1
    
    assert dur >= 0, 'Duration should be zero or positive.'
    return seconds_to_timestamp(dur)