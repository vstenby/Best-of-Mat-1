import numpy as np

def seconds_to_timestamp(seconds):
    '''
    Convert the seconds to HH:MM:SS:SSS timestamp.
    '''
    
    #If we pass a timestamp, then we just do nothing
    if type(seconds) is str: return seconds

    assert (type(seconds) is int) or (type(seconds) is float), 'seconds should either be an int or a float.'
    assert seconds >= 0, 'seconds should be equal to or larger than 0.'
    
    sss = np.round(seconds - np.floor(seconds),2)

    m, s = divmod(np.floor(seconds), 60)
    h, m = divmod(m, 60)

    sss = str(sss).split('.')[-1].ljust(2,'0')

    h = str(int(h)).zfill(2); m = str(int(m)).zfill(2); s = str(int(s)).zfill(2);

    return ':'.join([h,m,s]) + '.' + sss