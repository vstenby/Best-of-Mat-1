def timestamp_to_seconds(ts):
    '''
    Converts a timestamp to seconds.
    '''
    
    #If the type is either a float or integer, then just return the timestamp.
    if (type(ts) is float) or (type(ts) is int): return ts
    
    assert type(ts) is str, 'ts should be a string.'
    assert ts.count(':') <= 2, f"Too many :'s in the timestamp: {ts}"
    assert ts.count('.') <= 1, f"Too many .'s in the timestamp: {ts}"
    
    sss_ = 0
    
    if ts.count('.') == 1:
        ts, sss = ts.split('.')
        sss_ = 0
        for i, n in enumerate(sss):
            sss_ += 1/(10**(i+1)) * float(n)
            
    seconds = float(sum(int(x) * (60**i) for i, x in enumerate(reversed(ts.split(':'))))) + sss_
    
    assert 0 <= seconds, f"Something went wrong with loading the timestamp. {ts}"
    
    return seconds