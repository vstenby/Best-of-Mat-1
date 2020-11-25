#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- Dependencies -- 
import sys
import os
import numpy as np
import time

from bom1 import *
from settings import *

#These packages usually cause the most trouble.
import moviepy
import selenium
import youtube_dl

#Import DTU-Video-Downloader
sys.path.insert(1, 'DTU-Video-Downloader')
try:
    import DTU_VD_functions  as VDfunc
except ImportError:
    raise ImportError('Unable to import DTU-Video-Downloader. '\
                      +'Download it here: https://github.com/vstenby/DTU-Video-Downloader '\
                      +'and check folder structure.')
        
#Check if chromedriver exists
if not os.path.exists('chromedriver'):
    raise ImportError('chromedriver not found. Download the corresponding version here: https://chromedriver.chromium.org/downloads')

def main():
    
    #Check if ./download and ./export are folders
    needed_folders = ['./downloads', './export']
    for folder in needed_folders:
        if not os.path.exists(folder): os.mkdir(folder)
    
    #Generate df with all information
    df = generate_df()
    
    if not settings['clips'] == 'all':
        #Extract the clips that we need.
        clips = np.array(settings['clips'])
        df = df.loc[np.isin(df['name'].to_numpy(),clips)]
        
        #Clips specified in settings:
        clips_found = clips[np.isin(clips, df['name'].to_numpy())]
        print('Clipping the following clip(s):')
        for clipf in clips_found: print(clipf)
        print('')
        
        
        #Check that all of the clips were found.
        clips_not_found = clips[np.invert(np.isin(clips,df['name'].to_numpy()))] 
        if len(clips_not_found) != 0:
            print('Error finding the following clip(s):')
            for clipnf in clips_not_found:
                print(clipnf)
            print('')
        
    #Extract valid clips.
    df = df.loc[df['rating'].to_numpy() >= settings['min_rating']]
    df = df.loc[(df['t2'].to_numpy() - df['t1'].to_numpy()) <= settings['max_duration']]
    
    if settings['semesters'] == 'all': 
        settings['semesters'] = [x for x in os.listdir('./tsv') if not x.startswith('.')]
        
    df = df.loc[np.isin(df.semester.to_numpy(), settings['semesters'])]
    
    driver = None
    
    if len(df) == 0: 
        print('No clips to be clipped')
        return
    else:
        print(f'A total of {len(df)} clips were found to be exported.')
        
    for i in range(len(df)):
        
        clippath = df['clippath'].iloc[i] + settings['outputtype']
        if os.path.exists(clippath):
            #This clip already exists and therefore, it should be skipped.
            continue
    
        lecturepath = df['path'].iloc[i]
        
        # -- Download check  --
        if not os.path.exists(lecturepath):
            #Clear the downloaded folder
            for file in os.listdir('./downloads/'): 
                os.remove('./downloads/' + file)

            link = df['link'].iloc[i]; 
            if driver is None:
                print('It looks like we need to download a video!')
                config = VDfunc.prompt_config()
                driver = VDfunc.open_driver(config, 'https://video.dtu.dk/user/login')
    
            #Download video
            VDfunc.download_videos(driver, [link], pathout = [lecturepath.replace('.mp4', '')])
        # -- End of download check --
        
        t1 = df['t1'].iloc[i]
        t2 = df['t2'].iloc[i]
        
        #Do the actual clipping
        print(type(lecturepath))
        print(type(clippath))
        print(type(t1))
        print(type(t2))
        clip(lecturepath, t1, t2, clippath)

                
if __name__ == '__main__':
    main()