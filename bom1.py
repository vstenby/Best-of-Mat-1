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
import re

def clip(pathin, t1 : int, t2 : int, pathout):
    if t2 < t1: 
        return
    
    clip = VideoFileClip(filename=pathin).subclip(t1,t2)
    
    if pathout.endswith('.mp4'):
        clip.write_videofile(pathout, temp_audiofile="./export/temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
        clip.close()
    elif pathout.endswith('.mp3'):
        audio = clip.audio
        audio.write_audiofile(pathout)
        audio.close()
    
    
def fetch_semesters():
    semesters = os.listdir('./tsv')
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
        csvs = os.listdir('./tsv/' + semester); 
        csvs = [x for x in csvs if x.endswith('.tsv') and x != 'links.tsv']
       
        for csv in csvs:
            dftemp = pd.read_csv('./tsv/'+semester+'/'+csv,sep='\t',encoding='utf-8')
            dftemp['lecture']  = csv.replace('_',' ').replace('.tsv','')
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
            dftemp = pd.read_csv('./tsv/' + semester + '/links.tsv',sep='\t',encoding='utf-8')
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
    
def generate_df():
    df_clip = read_all_clips(); #df_clip['lecture'] = df_clip['lecture'].apply(lambda x : unicodedata.normalize('NFD', x))
    df_link = read_all_links(); #df_link['lecture'] = df_link['lecture'].apply(lambda x : unicodedata.normalize('NFD', x))
    
    df = pd.merge(df_clip, df_link, how='left', on=['lecture','semester'])
    df = df.sort_values(['semester','n'])
    
    df['path'] = './downloads/' + df['semester'] + '_' + df['n'].astype(str).str.zfill(2) + '_' + df['lecture'].str.replace(' ','_') + '.mp4'
    df['clippath'] = './export/' + df['semester'] + ' L' + df['n'].astype(str).str.zfill(2) + ' C' + df['clipnumber'].astype(str).str.zfill(2)+' R' + df['rating'].astype(str).str.zfill(2)+' '+df['name']
    
    #Convert timestamps
    df['t1'] = df['t1'].apply(lambda x : convert_timestamp(x))
    df['t2'] = df['t2'].apply(lambda x : convert_timestamp(x))
    
    if os.name == 'nt':
        df['name'] = df['name'].apply(lambda x : re.sub(r'[\\/*?:"<>|]',"",x))

    return df
    
    
        
    
        
    
    
