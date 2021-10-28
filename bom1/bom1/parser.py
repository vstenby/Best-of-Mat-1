import argparse
import numpy as np

def parser():
    #Set up the arguments. 
    parser = argparse.ArgumentParser()
    parser.add_argument('--clip-name', default=None, type=str, help='specify which clip name you want to export.')
    parser.add_argument('--min-rating', default=1, type=int,  choices = range(1,11), help='only export clips with rating >= minrating.')
    parser.add_argument('--max-rating', default=10, type=int, choices = range(1,11), help= 'only export clips with rating <= maxrating.') #Why anyone ever would use this, I don't know.
    parser.add_argument('--min-duration', default=0, type=int, help= 'only export clips with duration >= minduration. duration is in seconds.')
    parser.add_argument('--max-duration', default=np.inf, type=int, help='only export clips with duration <= maxduration. duration is in seconds.')
    parser.add_argument('--tag', default='', type=str, help='regex for specfiying which tag you want to export.')
    
    parser.add_argument('--min-t1', default=0, type=int, help='only export clips with mint1 <= t1.')
    parser.add_argument('--max-t1', default=np.inf, type=int, help='only export clips with t1 <= maxt1.')
    parser.add_argument('--min-t2', default=0, type=int, help='only export clips with mint2 <= t2.')
    parser.add_argument('--max-t2', default=np.inf, type=int, help='only export clips with t2 <= maxt2.')
    
    parser.add_argument('--prepad', default=0, type=float, help='pads the start of the clip with <prepad> seconds.')
    parser.add_argument('--postpad', default=0, type=float, help='pads the end of clip with <endpad> seconds.')
    
    parser.add_argument('--file-type', default='mp3', type=str, choices=['mp3', 'mp4', 'gif', 'wav'], help='filetype to export as either mp3, mp4 or gif.')
    parser.add_argument('--no-prefix', default=False,  action='store_true', help='include prefix specifying info about the clip.')
    parser.add_argument('--clear-export', default=False, action='store_true', help='clear the export folder before exporting.')
    
    parser.add_argument('--list', default=False, action='store_true', help='prints the list instead of clipping.')
    parser.add_argument('--load-empty', default=False, action='store_true', help='if --load-empty is passed, then csvs located in the "empty" csv folder are also loaded.')
    parser.add_argument('--include-placeholder', default=False, action='store_true', help='if --include-placeholder is passed, then placeholders are included.')
    parser.add_argument('--threads', default=4, type=int, help='Amount of threads used to download clips, default 4')
    parser.add_argument('--ar', default=44100, type=int, help='Sample rate of audio clips')
    
    
    #Should be grouped together as well.
    parser.add_argument('--silent', default=False, action='store_true', help='if --silent is passed, nothing is printed to the console.')
    parser.add_argument('--desc', default='Exporting clips', type=str, help='Description of the progress bar')
    
    #Add normalize and no-normalize
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--normalize',    default=True,  action='store_true', help='normalize the audio of the output clip. this only works with mp4 at the moment.')
    group.add_argument('--no-normalize', default=False, action='store_true', help='dont normalize the audio of the output clip.')
    
    #TODO: Add some more arguments. 
    return parser