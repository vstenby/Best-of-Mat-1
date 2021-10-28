import bom1 
import os

def test_clip():
    bom1.clip([0], [5], ['https://video.dtu.dk/media/Komplekse+Tal+del1/0_nh2pvfdd/200597'], ['test.wav'])
    os.remove('test.wav')