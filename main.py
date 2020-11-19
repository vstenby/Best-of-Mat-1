#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:53:13 2020

@author: viktorstenby
"""

import numpy as np
from bom1 import *

def main():
    import sys
    import os
    
    sys.path.insert(1, 'DTU-Video-Downloader')
    import DTU_VD_functions  as VDfunc   
    
    #Check if ./download and ./export are folders
    needed_folders = ['./downloads', './export']
    for folder in needed_folders:
        if not os.path.exists(folder): os.mkdir(folder)
        
    #Fetch input arguments
    argin = sys.argv[1:]; argin = [x.strip().lower() for x in argin]
    
    #Work in progress - should be able to hand multiple keywords later.
    if len(argin) == 0: 
        mainarg = 'clip'
    else:
        mainarg = argin[0]
        argin = argin[1:]
    
    if mainarg == 'clip':
        df_clip = read_all_clips(); #df_clip['lecture'] = df_clip['lecture'].apply(lambda x : unicodedata.normalize('NFD', x))
        df_link = read_all_links(); #df_link['lecture'] = df_link['lecture'].apply(lambda x : unicodedata.normalize('NFD', x))
        
        df_full = pd.merge(df_clip, df_link, how='left', on=['lecture','semester'])
        df_full = df_full.sort_values(['semester','n'])
        
        #df_clip['downloaded'] = df_clip.apply(lambda x : x['semester']+'_'+)
        df_full['path'] = './downloads/' + df_full['semester'] + '_' + df_full['n'].astype(str).str.zfill(2) + '_' + df_full['lecture'] + '.mp4'
        
        lecture_need = df_full['path'].to_numpy()
        lecture_have = np.asarray(['./downloads/' + x.replace('.mp4','').replace('_',' ') for x in os.listdir('./downloads') if not x.startswith('.')])
        
        df_full['downloaded'] = np.isin(lecture_need,lecture_have)
        
        df_full['clippath'] = './export/' + df_full['semester'] + ' L' + df_full['n'].astype(str).str.zfill(2) + ' C' + df_full['clipnumber'].astype(str).str.zfill(2)+' R' + df_full['rating'].astype(str).str.zfill(2)+' '+df_full['name']
        
        if '.mp3' in argin:
            df_full['clippath'] += '.mp3'
        else:
            df_full['clippath'] += '.mp4'
            
        #Convert timestamps
        df_full['t1'] = df_full['t1'].apply(lambda x : convert_timestamp(x))
        df_full['t2'] = df_full['t2'].apply(lambda x : convert_timestamp(x))
        
        driver = None
        for i in range(len(df_full)):
            downloaded = df_full['downloaded'].iloc[i]
            if not downloaded:
                link = df_full['link'].iloc[i]
                path = df_full['path'].iloc[i].replace(' ','_')
                
                if driver is None:
                     print('It looks like we need to download some videos!')
                     config = VDfunc.prompt_config()
                     driver = VDfunc.open_driver(config, 'https://video.dtu.dk/user/login')
                    
                VDfunc.download_videos(driver,[link],pathout=[path.replace('.mp4','')])
                    
                #Update the dataframe to show we have downloaded said video
                downloadstatus = df_full['downloaded'].to_numpy()
                videopaths = df_full['path'].to_numpy()
                downloadstatus[videopaths == path] = True
                df_full['downloaded'] = downloadstatus
            
            lecturepath = df_full['path'].iloc[i].replace(' ','_')
            t1 = df_full['t1'].iloc[i]
            t2 = df_full['t2'].iloc[i]
            clippath = df_full['clippath'].iloc[i]
            
            #Do the actual clipping
            clip(lecturepath, t1, t2, clippath)
            
            #Remove the downloaded lecture if need be. 
            if i != len(df_full)-1:
                if df_full['lecture'][i] != df_full['lecture'][i+1]:
                    os.remove(lecturepath)
            else:
                os.remove(lecturepath)
                   
if __name__ == '__main__':
    main()