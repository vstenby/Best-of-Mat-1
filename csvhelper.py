#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Dependencies
import os
import numpy as np
import pandas as pd
from bom1 import *
import argparse
import sys


def main():
    '''
    csvhelper helps with the csv folder structure.
    '''

    #Set up the arguments. 
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', default=None, type=str, help='adds a new lecture to metadata and csvs. syntax is --add "<tag> <url>" or --add <file.txt> where the file contains rows, where each row has a tag and a url.')
    parser.add_argument('--changetag', default=None, type=str, help='changes the tag, e.g: --changetag "E17B_L01 E99B_L99"')
    args = parser.parse_args()
    
    if len(sys.argv) <= 1:
        print('csvhelper.py should be called with one argument.')
        return
        
    if args.add is not None:
        if args.add.endswith('.txt') and len(args.add.split(' ')) == 1:
            tags  = list(np.loadtxt('newtags.txt', dtype='str')[:,0])
            links = list(np.loadtxt('newtags.txt', dtype='str')[:,1])
        else:
            try:
                tag, link = args.add.split(' ')
                tags = [tag]
                links = [link]
            except:
                raise ValueError(f'args.add should consist of a tag and link part')
        
        #Make sure the tag is valid and it doesn't already exist in ./csv/
        for tag in tags:
            check_tag(tag)
            for csv in os.listdir('./csv'):
                assert tag not in csv, f'Tag {tag} already found in ./csv/: ./csv/{csv}. It cannot be added.'
      
        #Fetch url from link.
        (stream_titles, stream_links, download_links) = fetch_info(links)
        metadata = pd.read_csv('./csv/metadata.csv')
        
        for tag, stream_title, link, stream_link, download_link in zip(tags, stream_titles, links, stream_links, download_links):
            metadata = metadata.append(pd.DataFrame({'tag' : tag, 
                                                     'stream_title' : stream_title, 
                                                     'link' : link, 
                                                     'stream_link' : stream_link, 
                                                     'download_link' : download_link}, index=[0]), ignore_index = True)
            
            
            pd.DataFrame({'name' : 'Placeholder', 't1' : '00:00:00', 't2' : '00:00:01', 'rating' : 0}, index=[0]).to_csv(f'./csv/{tag} {stream_title}.csv', index=False, sep=',')
            print(f'{tag} added to ./csv/metadata.csv with title {stream_title}')
            
            
            
            
        metadata.to_csv('./csv/metadata.csv', index=False, sep=',')
        
    if args.changetag is not None:
        tag_from, tag_to = args.changetag.split(' ')
        
        #Check that both tag_from and tag_to are valid tags.
        check_tag(tag_from)
        check_tag(tag_to)
        
        try:
            path_from = ['./csv/' + x for x in os.listdir('./csv/') if tag_from in x][0]
        except:
            raise ValueError(f'No file with tag {tag_from}.')
            
        path_to   = path_from.replace(tag_from, tag_to)
        
        assert path_from != path_to, 'path from and path to should not be the same.'
        
        process = subprocess.Popen(["git", "mv", path_from, path_to], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        
        #Replace it in metadata as well.
        metadata = pd.read_csv('./csv/metadata.csv')
        metadata['tag'] = metadata['tag'].replace({tag_from : tag_to})
        metadata.to_csv('./csv/metadata.csv', sep=',', index=False)
        print(f'{path_from} moved to {path_to} and metadata.csv updated. Check git status.')
        
    return

if __name__ == '__main__':
    main()

