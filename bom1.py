#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import time
import subprocess
import os

import threading
import queue

def welcome():
    st=["""
      ____            _            __   __  __       _     __ 
     |  _ \          | |          / _| |  \/  |     | |   /_ |
     | |_) | ___  ___| |_    ___ | |_  | \  / | __ _| |_   | |
     |  _ < / _ \/ __| __|  / _ \|  _| | |\/| |/ _` | __|  | |
     | |_) |  __/\__ \ |_  | (_) | |   | |  | | (_| | |_   | |
     |____/ \___||___/\__|  \___/|_|   |_|  |_|\__,_|\__|  |_|
        """,
        '     '+'Best of Mat 1: Release 3.0.0 (24/10/2021)'.center(57),
        '',
        'Author: Viktor Stenby Johansson',
        'If you have any problems with this software, feel free to reach out to me via Facebook.',
        '']
    for s in st: print(s)
    return

def load_clips(load_empty=False):
    #Read in the metadata which contains semester tag, name and url.
    metadata = pd.read_csv('./csv/metadata.csv',sep=',')

    csvs = [os.path.join('./csv/filled/',x) for x in os.listdir('./csv/filled') if (x.endswith('.csv'))]
    
    if load_empty:
        #Then we also load the csvs located in the "empty" folder.
        empty = [os.path.join('./csv/empty',x) for x in os.listdir('./csv/empty') if (x.endswith('.csv'))]
        csvs += empty
        
    
    #Sort by all sorts of stuff. Basically make sure that the csvs are loaded in the right order.
    csvs.sort(key = lambda element: (int(os.path.basename(element)[1:3]), reversor(os.path.basename(element)[0]), os.path.basename(element)[3], os.path.basename(element)[6:8]))

    clips = pd.DataFrame(columns=['tag', 'nclip', 'name', 't1', 't2', 'rating'])

    for csv in csvs:
        temp = pd.read_csv(csv, sep=',')
        
        #Fetch the basename.
        csv = os.path.basename(csv)
        
        temp['tag'] = csv.split(' ')[0]
        temp['nclip'] = np.arange(1, len(temp)+1)
        
        #Make sure we don't get any of them nans.
        if np.any(pd.isna(temp)):
            raise ValueError(f'NaN found in {csv}.')
            
        clips = clips.append(temp)

    clips = clips.merge(metadata, on='tag')
    clips['duration'] = [timestamp_to_seconds(y) - timestamp_to_seconds(x) for x, y in zip(clips['t1'], clips['t2'])]    
    clips['name'] = clips['name'].apply(lambda x : x.strip())

    assert np.all(clips['duration'] >= 0), 'Clips found with negative duration.'
    
    return clips
                                                                
#Class used to sort the csvs.
class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj


def timestamp_to_seconds(ts):
    '''
    Converts a timestamp to seconds.
    '''
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

def seconds_to_timestamp(seconds):
    '''
    Convert the seconds to HH:MM:SS:SSS timestamp.
    '''
    sss = np.round(seconds - np.floor(seconds),2)

    m, s = divmod(np.floor(seconds), 60)
    h, m = divmod(m, 60)

    sss = str(sss).split('.')[-1].ljust(2,'0')

    h = str(int(h)).zfill(2); m = str(int(m)).zfill(2); s = str(int(s)).zfill(2);

    return ':'.join([h,m,s]) + '.' + sss
    
def duration(t1, t2):
    t1  = timestamp_to_seconds(t1)
    t2  = timestamp_to_seconds(t2)
    dur = t2-t1
    
    assert dur >= 0, 'Duration should be zero or positive.'
    return seconds_to_timestamp(dur)
     
def print_clips(clips):
    if len(clips) == 0:
        return
    clips = clips.reset_index(drop=True)
    print('Tag'.center(10) + 'Name'.ljust(100) + 'Rating')
    print('-'*(10+100+6))
    prev_tag = clips['tag'][0]
    for tag, name, rating in zip(clips['tag'], clips['name'], clips['rating']):
        if tag != prev_tag:
            print('')
        prev_tag = tag
        print(tag.ljust(10) + name.ljust(100) + str(rating).rjust(6))
    return

def stream_link(ID):
    '''
    Fetches a stream link from ID. 
    '''
    return f'https://dchsou11xk84p.cloudfront.net/p/201/sp/20100/playManifest/entryId/{ID}/format/url/protocol/https'
    
def download_link(ID):
    '''
    Returns a download link from ID.
    '''
    return f'https://dchsou11xk84p.cloudfront.net/p/201/sp/20100/playManifest/entryId/{ID}/format/download/protocol/https/flavorParamIds/0'

def get_duration(url):
    '''
    Returns the duration of a video.
    '''
    import cv2 as cv
    
    #Read the video capture from cv2.
    cap = cv.VideoCapture(stream_link(fetch_ID(url)))
    return int(cap.get(cv.CAP_PROP_FRAME_COUNT))/cap.get(cv.CAP_PROP_FPS)

def fetch_ID(url):
    '''
    Takes a video.dtu.dk link and returns the video ID.
    
    TODO: This should make some assertions about the url.
    '''
    return '0_' + url.split('0_')[-1].split('/')[0]

def fix_outpath(path):
    '''
    Fixes the path out by removing letters that cause issues when exporting.
    '''
    pathout = path.replace(' ','_')\
                  .replace(',','')\
                  .replace("'","")\
                  .replace(')','').replace('(','')
    
    return pathout

def ffmpeg_clip(t1, t2, url, pathout, normalize=False):
    '''
    Export a clip.
    Input:
        t1:  start time (seconds)
        t2:  end time (seconds)
        url: video.dtu.dk link
    '''
    assert 0 <= t1, f'Invalid value of t1: {t1}'
        
    #Replace letters causing trouble.
    pathout = fix_outpath(pathout)
    
    t1_timestamp = seconds_to_timestamp(t1) 
    t2_timestamp = seconds_to_timestamp(t2) 
    duration = seconds_to_timestamp(t2-t1) 
    
    #Get the stream url from the video.dtu.dk url.
    url = stream_link(fetch_ID(url))
    
    if pathout.endswith('.mp3') or pathout.endswith('.wav'):
        bashcmd = f'ffmpeg -y -ss {t1_timestamp} -i "{url}" -t {duration} -q:a 0 -map a {pathout} -loglevel error'
    elif pathout.endswith('.mp4') or pathout.endswith('.gif'):
        bashcmd = f'ffmpeg -y -ss {t1_timestamp} -i "{url}" -t {duration} {pathout} -loglevel error'
    else:
        raise ValueError('Wrong output format.')
            
    rtrn = subprocess.call(bashcmd, shell=True)
    
    if normalize and pathout.endswith('.mp4'):
        #This might fail if you don't have ffmpeg-normalize installed. pip3 install ffmpeg-normalize. Normalization also only seems to work with mp4.
        normalize_rtrn = subprocess.call(f'ffmpeg-normalize {pathout} -o {pathout} -c:a aac -b:a 192k -f', shell=True, 
                                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
    return rtrn

def check_tag(tag):
    '''
    Checks the syntax of tags.
    '''
    
    assert len(tag) == 7, f'Error with {tag}: tag should have length 7.'
    assert tag[0] in ['E', 'F'], f'Error with {tag}: the first character of the tag should either be E (Efterår) or F (Forår)'
    try:
        year = int(tag[1:2])
        assert year >= 0, f'{tag} is an invalid tag.'
    except:
        raise ValueError(f'Error with {tag}: tag[1:2] should be numbers specifying the year.')
    
     #This will exclude GEs, but we'll cross that bridge when we get to it...
    assert tag[3] in ['A', 'B', 'C'], f'Error with {tag}: tag[3] should specify the skema, either A, B or C.'
    assert tag[4] == 'L', f'{tag} is an invalid tag.'

    try: 
        lecture_number = int(tag[5:7])
        assert lecture_number >= 1
    except:
        raise ValueError(f'Error with {tag}: tag[5:7] should be numbers specifying the lecture. First lecture number is 01.')

    return

#Set the count for exporting in parallel.
count = 0

def export(t1, t2, url, outpath, i, args, n, ):
#Convert t1 and t2 to seconds and subtract the prepadding and postpadding.
    t1, t2 = timestamp_to_seconds(t1) - args.prepad, timestamp_to_seconds(t2) + args.postpad
    
    rtrn = ffmpeg_clip(t1,t2,url,outpath, normalize=args.normalizeaudio)

    global count
    count += 1
    if not args.silent:
        if not rtrn:
            #Replace letters causing trouble.
            outpath = fix_outpath(outpath)
            print((str(count)+'/'+str(n)).ljust(9)+ f'{outpath} succesfully exported.')
        else:
            print((str(count)+'/'+str(n)).ljust(9)+ f'{outpath} was not exported.')

    return

#worker threads for queues
def workerThread(q):
    while True:
        args = q.get()[0:]
        export(*args)
        q.task_done()

    return

def export_clips(clips, args):
    q = queue.Queue(0)
    num_threads = args.threads if args.threads > 0 else 1
    n = len(clips)
    
    for t1, t2, url, outpath, i in zip(clips['t1'], clips['t2'], clips['link'], clips['outpath'], range(0, n)):
        q.put((t1,t2,url,outpath,i, args, n,))
    for _ in range(num_threads):
        worker = threading.Thread(target=workerThread, args=(q,))
        worker.setDaemon(True)
        worker.start()

    q.join()
    
    return 