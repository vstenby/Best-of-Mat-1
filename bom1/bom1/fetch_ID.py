def fetch_ID(url):
    '''
    Takes a video.dtu.dk link and returns the video ID.
    
    TODO: This should make some assertions about the url.
    '''
    return '0_' + url.split('0_')[-1].split('/')[0]