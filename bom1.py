#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np

def welcome():
    st=["""
      ____            _            __   __  __       _     __ 
     |  _ \          | |          / _| |  \/  |     | |   /_ |
     | |_) | ___  ___| |_    ___ | |_  | \  / | __ _| |_   | |
     |  _ < / _ \/ __| __|  / _ \|  _| | |\/| |/ _` | __|  | |
     | |_) |  __/\__ \ |_  | (_) | |   | |  | | (_| | |_   | |
     |____/ \___||___/\__|  \___/|_|   |_|  |_|\__,_|\__|  |_|
        """,
        '     '+'Best of Mat 1: Release 2.1.0 (24/04/2021)'.center(57),
        '',
        'Author: Viktor Stenby Johansson',
        'If you have any problems with this software, feel free to reach out to me via Facebook.',
        '']
    for s in st: print(s)
    return

def load_clips():
    #Read in the metadata, download links etc. etc.
    metadata = pd.read_csv('./csv/metadata.csv',sep='\t')

    csvs = [x for x in os.listdir('./csv') if (x.endswith('.csv')) and (x != 'metadata.csv')]
    
    #Sort by all sorts of stuff. Basically make sure that the csvs are loaded in the right order.
    csvs.sort(key = lambda element: (int(element[1:3]), reversor(element[0]), element[3], element[6:8]))

    clips = pd.DataFrame(columns=['tag', 'nclip', 'name', 't1', 't2', 'rating'])

    for csv in csvs:
        temp = pd.read_csv('./csv/'+csv, sep='\t')
        temp['tag'] = csv.split(' ')[0]
        temp['nclip'] = np.arange(1, len(temp)+1)
        clips = clips.append(temp)

    clips = clips.merge(metadata, on='tag')
    clips['duration'] = [ts_to_int(duration(x,y)) for x, y in zip(clips['t1'], clips['t2'])]
    clips['name'] = clips['name'].apply(lambda x : x.strip())
    
    return clips
                                                                   

                                             
def fetch_info(urls):
    from getpass import getpass
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import os
    import json
    
    '''
    Input: 
        urls, either a single or list of urls pointing to a lecture,
        e.g. https://video.dtu.dk/media/Uge+11A+Symmetriske+matricer+-+del+1/0_knty601o/185135
        
    Output:
        (stream_titles, stream_links, download_links)
        stream_titles  are the lecture title, where ':', ',' and '.' is removed.
        stream_links   are the links to the streamed version of the lecture.
        download_links are the links to downloading the lecture. 
    '''
    
    username = input("Please enter your DTU login: ")
    password = getpass("Please enter your DTU password: ")
    
    if not os.path.isfile('./chromedriver'):
            raise Exception('Chromedriver cannot be located.')
            
    # Specify window to not open
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome('./chromedriver',options=options)

    driver.get('https://video.dtu.dk/user/login')

    elem = driver.find_element_by_name('Login[username]')
    elem.clear()
    elem.send_keys(username)

    elem = driver.find_element_by_name('Login[password]')
    elem.clear()
    elem.send_keys(password)

    print('Logging into video.dtu.dk!')
    elem.send_keys(Keys.RETURN)

    try:
        elem = driver.find_element_by_class_name('formError')
        print('Wrong username or password.')
    except:
        print('Succesfully logged into video.dtu.dk!')
        
    if type(urls) is not list: urls = [urls]
    
    stream_titles   = []
    stream_links    = []
    download_links  = []
    
    for i, url in enumerate(urls):
        
        #Move driver to that url.
        driver.get(url)
        
        stream_titles.append(driver.find_element_by_class_name('entryTitle').text\
                                   .replace(':','').replace(',','')\
                                   .replace('Ã¥', 'aa').replace('Ã¦', 'ae')) 
                                    #We might need to replace more letters eventually.
        
        driver.switch_to.frame(driver.find_element_by_css_selector('#kplayer_ifp'))
        script = driver.find_element_by_css_selector('body script:nth-child(2)').get_attribute("innerHTML")
        data = (script.splitlines()[2])[37:-1]
        
        # Load the data into json format
        js = json.loads(data)
        
        #Get the stream link and download link.
        stream_links.append(js["entryResult"]["meta"]["dataUrl"])
        download_links.append(js["entryResult"]["meta"]["downloadUrl"])
        print(f'Info fetched for video {i+1}/{len(urls)}', end='\r')
        
    #If we only queried for one url.
    if len(stream_titles) == 1: 
        stream_titles  = stream_titles[0]
        stream_links   = stream_links[0]
        download_links = download_links[0]
    
    return stream_titles, stream_links, download_links

#Class used to sort the csvs.
class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj

def ts_to_int(ts):
    '''
    Helper function to convert timestamp to int.
    '''
    if type(ts) is str:
        if ':' in ts:
            #We either have HH:MM:SS or HH:SS
            if ts.count(':') == 1:
                #MM:SS
                hh     = 0
                mm, ss = ts.split(':')
                mm, ss = int(mm), int(ss)

            elif ts.count(':') == 2:
                #HH:MM:SS
                hh, mm, ss = ts.split(':')
                hh, mm, ss = int(hh), int(mm), int(ss)
        #Check that mm < 60 and ss < 60.
        if not ((mm < 60) and (ss < 60)):
            raise ValueError(f'Minute or second count is more than 60. Given timestamp: {ts}.')
        s = ss + mm*60 + hh*60*60
    else:
        s = int(ts)
    return s

def duration(t1, t2):
    
    diff = ts_to_int(t2) - ts_to_int(t1)
    
    #Clip is between 0 seconds and 1 hour.
    assert (diff > 0) and (diff < 3600)

    minutes, seconds = divmod(diff, 60)

    return f'{minutes:02}:{seconds:02}'

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

def ffmpeg_clip(t1, t2, url, pathout, normalize=False):
    import subprocess
    
    #Replace letters causing trouble.
    pathout = pathout.replace(' ','_')\
                     .replace(',','')\
                     .replace("'","") 
    
    if pathout.endswith('.mp3'):
        bashcmd = f'ffmpeg -ss 00:{t1}.00 -i "{url}" -t 00:{duration(t1,t2)}.00 -q:a 0 -map a {pathout} -loglevel error'
    elif pathout.endswith('.mp4'):
        #bashcmd = f'ffmpeg -ss 00:{t1}.00 -i "{url}" -t 00:{duration(t1,t2)}.00 -c copy {pathout} -loglevel error'
        bashcmd = f'ffmpeg -ss 00:{t1}.00 -i "{url}" -t 00:{duration(t1,t2)}.00 {pathout} -loglevel error'
    else:
        raise ValueError('Wrong output format.')
            
    rtrn = subprocess.call(bashcmd, shell=True)
    
    if normalize and pathout.endswith('.mp4'):
        #This might fail if you don't have ffmpeg-normalize installed. pip3 install ffmpeg-normalize. Normalization also only seems to work with mp4.
        normalize_rtrn = subprocess.call(f'ffmpeg-normalize {pathout} -o {pathout} -c:a aac -b:a 192k -f', shell=True, 
                                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
    return rtrn