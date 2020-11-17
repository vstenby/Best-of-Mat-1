#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 17:19:05 2020

@author: viktorstenby
"""

import moviepy
from moviepy.editor import VideoFileClip
import pandas as pd
import os
import unicodedata
import numpy as np

def clip(pathin, t1 : int, t2 : int, pathout):
    if t2 < t1: 
        return
    
    clip = VideoFileClip(filename=pathin).subclip(t1,t2)
    
    if pathout.endswith('.mp4'):
        #pathout = pathout.replace('.mp4','')
        clip.write_videofile(pathout, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
        #clip.write_videofile(pathout)
    elif pathout.endswith('.mp3'):
        #pathout = pathout.replace('.mp3','')
        clip.write_audiofile(pathout)
    
    
def fetch_semesters():
    semesters = os.listdir('./csv')
    semesters = [x for x in semesters if x.startswith('E') or x.startswith('F')]
    return semesters
    
def convert_timestamp(s):
    #MM:SS or HH:MM:SS
    ssplit = s.split(':'); ssplit = [int(x) for x in ssplit]
    if len(ssplit) == 2:
        if ssplit[0] > 59 or ssplit[1] > 59: 
            raise ValueError('Invalid timestamp.')
        return ssplit[0]*60 + ssplit[1]
    elif len(ssplit) == 3:
        #HH:MM:SS
        if ssplit[1] > 59 or ssplit[2] > 59: 
            raise ValueError('Invalid timestamp.')
        return ssplit[0]*60*60 + ssplit[1]*60 + ssplit[2]
    else:
        raise ValueError('Wrong number of : in string')
    
    
def read_clips(semesters):
    
    df = pd.DataFrame(columns=['t1','t2','name','rating','semester','clipnumber'])
    
    for semester in semesters:
        csvs = os.listdir('./csv/' + semester); 
        csvs = [x for x in csvs if x.endswith('.csv') and x != 'links.csv']
       
        for csv in csvs:
            dftemp = pd.read_csv('./csv/'+semester+'/'+csv,sep=';',encoding='utf-8')
            dftemp['lecture']  = csv.replace('_',' ').replace('.csv','')
            dftemp['semester'] = semester
            dftemp['clipnumber'] = np.arange(len(dftemp))+1
            df = df.append(dftemp)
            
    df = df.reset_index(drop=True)

    return df

def read_all_clips():
    semesters = fetch_semesters()
    df = read_clips(semesters)
    return df

def read_links(semesters):
    df = pd.DataFrame(columns=['n', 'lecture', 'link', 'semester'])
    for semester in semesters:
        try:
            dftemp = pd.read_csv('./csv/' + semester + '/links.csv',sep=';',encoding='utf-8')
            dftemp['semester'] = semester
        except:
            dftemp = pd.DataFrame(columns=['n', 'lecture', 'link', 'semester'])
            
        df = df.append(dftemp)
        
   
    return df

def read_all_links():
    semesters = fetch_semesters()
    df = read_links(semesters)
    return df

def start_driver():
    import sys
    sys.path.insert(1, 'DTU-Video-Downloader')
    import DTU_VD_functions  as VDfunc   
    
    config = VDfunc.prompt_config()
    driver = VDfunc.open_driver(config, 'https://video.dtu.dk/user/login')
    
    return driver

def download_links(df):
    links = list(df['link'])
    names = './downloads/' + df['semester'] + ' ' + df['n'].apply(lambda x : str(x).zfill(2)).astype(str) + ' ' + df['name']
    names = [x.replace(' ','_') for x in names]
    
    import sys
    sys.path.insert(1, '/DTU-Video-Downloader/DTU_VD_functions.py')
    
    config = prompt_config()
    driver = open_driver(config, 'https://video.dtu.dk/user/login')
    
    download_videos(driver,links,pathout=names)
    

    
    
    
    
        
    
        
    
    
