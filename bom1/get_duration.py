import cv2 as cv
from .stream_link import *
from .fetch_ID import *

def get_duration(url):
    '''
    Returns the duration of a video.
    '''
    
    #Read the video capture from cv2.
    cap = cv.VideoCapture(stream_link(fetch_ID(url)))
    return int(cap.get(cv.CAP_PROP_FRAME_COUNT))/cap.get(cv.CAP_PROP_FPS)