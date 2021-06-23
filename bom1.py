#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import time
import subprocess
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json

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
    metadata = pd.read_csv('./csv/metadata.csv',sep=',')

    csvs = [x for x in os.listdir('./csv') if (x.endswith('.csv')) and (x != 'metadata.csv') and (x != 'kan-i-se-det.csv')]
    
    #Sort by all sorts of stuff. Basically make sure that the csvs are loaded in the right order.
    csvs.sort(key = lambda element: (int(element[1:3]), reversor(element[0]), element[3], element[6:8]))

    clips = pd.DataFrame(columns=['tag', 'nclip', 'name', 't1', 't2', 'rating'])

    for csv in csvs:
        temp = pd.read_csv('./csv/'+csv, sep=',')
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

def ffmpeg_clip(t1, t2, url, pathout, normalize=False):
    #t1 and t2 are seconds here.
    assert 0 <= t1, f'Invalid value of t1: {t1}'
        
    #Replace letters causing trouble.
    pathout = pathout.replace(' ','_')\
                     .replace(',','')\
                     .replace("'","") 
    
    
    
    t1_timestamp = seconds_to_timestamp(t1) 
    t2_timestamp = seconds_to_timestamp(t2) 
    duration = seconds_to_timestamp(t2-t1) 
    
    if pathout.endswith('.mp3') or pathout.endswith('.wav'):
        bashcmd = f'ffmpeg -ss {t1_timestamp} -i "{url}" -t {duration} -q:a 0 -map a {pathout} -loglevel error'
    elif pathout.endswith('.mp4') or pathout.endswith('.gif'):
        bashcmd = f'ffmpeg -ss {t1_timestamp} -i "{url}" -t {duration} {pathout} -loglevel error'
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

class InfoFetcher():
    '''
    Class used for fetching information from video.dtu.dk.
    Not used in main.py, but used to fetch information for the metadata.csv file. 
    '''
    def __init__(self):
    
        assert os.path.isfile('./chromedriver'), 'Chromedriver was not located - make sure to download it!'
            
        #Log in on video.dtu.dk
        self.driver = self.open_driver()
        
        while True:
            rtrn = self.login()
            if rtrn == 0:
                break
        
        #Now, we have a driver that is logged in.
        
    def open_driver(self):
        '''
        Open the driver!
        '''
        # Specify window to not open
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        driver = webdriver.Chrome('./chromedriver',options=options)
        driver.get('https://video.dtu.dk/user/login')
        
        return driver

    def prompt_login(self):
        '''
        Prompt for login upon creating the VideoDownloader
        '''
        username    = input('Please enter your DTU login (sxxxxxx@student.dtu.dk)').strip()
        password    = getpass('Please enter your password').strip()
        
        return username, password
        
    def login(self):
        '''
        Logs in on video.dtu.dk
        '''
        
        username, password = self.prompt_login()
        
        #Enter username
        elem = self.driver.find_element_by_name('Login[username]')
        elem.clear()
        elem.send_keys(username)
        
        #Enter password
        elem = self.driver.find_element_by_name('Login[password]')
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        
        #Wait a second and see if it failed.
        time.sleep(1)
        
        try:
            elem = self.driver.find_element_by_class_name('formError')
            print('Login failed. Prompting again!')
            return 1
        except:
            print('Succesfully logged in.')
            return 0
        
    def category_to_lectures(self, category_url):
        '''
        Convert a category url to a list of lectures.
        '''
        assert 'category' in category_url, 'Category should be in category url.'
        
        #Load the url and wait a few seconds.
        self.driver.get(category_url)
        time.sleep(4)

        #Find how much media we're reading in.
        elem   = self.driver.find_element_by_xpath('/html/body/div/div[1]/div[4]/div[4]/div/div/div[1]/div[1]/div[2]/ul/li[1]/a')
        nmedia = int(elem.text.replace(' Media',''))
        
        assert nmedia > 1, 'Category should contain more than 1 url.'
        
        scrolling = True

        while scrolling:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            try:
                elem = self.driver.find_element_by_xpath('/html/body/div/div[1]/div[4]/div[4]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div/a')
                elem.click()
            except:
                pass

            try:
                elem = self.driver.find_element_by_xpath('/html/body/div/div[1]/div[4]/div[4]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]')
                scrolling = False
            except:
                pass

        #Scroll to the top and get all links.
        self.driver.execute_script("window.scrollTo(0, 0);")

        lecture_urls = []

        for idx in np.arange(1, nmedia+1):

            elem = self.driver.find_element_by_xpath('//*[@id="gallery"]/li[' + str(idx) + ']/div[1]/div[1]/div/p/a')
            self.driver.execute_script("arguments[0].scrollIntoView()", elem)
            link = elem.get_attribute('href')
            lecture_urls.append(link)

        assert nmedia == len(lecture_urls), f'Top said {nmedia} Media, but only {len(lecture_urls)} links found.'
        
        return lecture_urls
    
    def unpack_url(self, url):
        '''
        Input: 
            url (str)
        Returns:
            title, stream_url, download_url
        '''
        
        if 'category' in url:
            #If we give it a category url, then it should first make the category url to lecture urls.
            url = self.category_to_lectures(url)
        
        if type(url) is list:
            titles = []
            stream_urls = []
            download_urls = []
            
            for u in url:
                #Call this function recursively
                title, stream_url, download_url = self.unpack_url(u)
                
                #Append to the lists
                titles.append(title)
                stream_urls.append(stream_url)
                download_urls.append(download_url)
                
            #Return the lists.
            return titles, stream_urls, download_urls
            
        else:
            
            #Move driver to that url.
            self.driver.get(url)           

            #Replace some strange characters = 
            title = self.driver.find_element_by_class_name('entryTitle').text.replace(':','').replace(',','').replace('Ã¥', 'aa').replace('Ã¦', 'ae')

            self.driver.switch_to.frame(self.driver.find_element_by_css_selector('#kplayer_ifp'))
            script = self.driver.find_element_by_css_selector('body script:nth-child(2)').get_attribute("innerHTML")
            data = (script.splitlines()[2])[37:-1]

            # Load the data into json format
            js = json.loads(data)

            #Get the stream link and download link.
            stream_url   = js["entryResult"]["meta"]["dataUrl"]
            download_url = js["entryResult"]["meta"]["downloadUrl"]

            return title, stream_url, download_url