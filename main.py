#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Dependencies
import os
import numpy as np
import pandas as pd
import bom1.bom1 as bom1
import argparse
import difflib
import re

import time

def main():

    #Set up the arguments. 
    parser = bom1.parser()
    
    args = parser.parse_args()
    
    #A few assertions
    assert args.prepad >= 0, f'args.prepad should be 0 or greater. args.prepad: {args.prepad}'
    assert args.postpad >= 0, f'args.postpad should be 0 or greater. args.postpad: {args.postpad}'
    
    if not args.silent:
        #Print the welcome message.
        bom1.welcome()
    
    #Load the clips
    clips = bom1.load_clips(load_empty = args.load_empty)
    
    n = len(clips)
    
    #Make sure that we have the ./export folder.
    if not os.path.exists('./export'):
        os.mkdir('./export')
    
    #Construct the masks for each query.
    if args.clip_name is not None:
        clipname_mask = (clips['name'].str.findall(args.clip_name).astype(bool)).to_numpy()
    else:
        clipname_mask = np.ones(n).astype(bool)
        
    if args.min_rating != 0:
        minrating_mask = (args.min_rating <= clips['rating']).to_numpy()
    else:
        minrating_mask = np.ones(n).astype(bool)

    if args.max_rating != 10:
        maxrating_mask = (clips['rating'] <= args.max_rating).to_numpy()
    else:
        maxrating_mask = np.ones(n).astype(bool)
        
    if args.min_duration != 0:
        minduration_mask = (args.min_duration <= clips['duration']).to_numpy()
    else:
        minduration_mask = np.ones(n).astype(bool)
        
    if args.max_duration != np.inf:
        maxduration_mask = (clips['duration'] <= args.max_duration).to_numpy()
    else:
        maxduration_mask = np.ones(n).astype(bool)
    
    if args.tag != '':
        tags = [tag for tag in clips['tag'].unique() if re.search(args.tag, tag) is not None]
        tags_mask = (clips['tag'].isin(tags)).to_numpy()
    else:
        tags_mask = np.ones(n).astype(bool)
        
    if args.min_t1 != 0:
        mint1_mask = args.min_t1 <= clips['t1'].apply(lambda x : timestamp_to_seconds(x)).to_numpy()
    else:
        mint1_mask = np.ones(n).astype(bool)
        
    if args.max_t1 != np.inf:
        maxt1_mask = clips['t1'].apply(lambda x : timestamp_to_seconds(x)).to_numpy() <= args.max_t1
    else:
        maxt1_mask = np.ones(n).astype(bool)
        
    if args.min_t2 != 0:
        mint2_mask = args.min_t2 <= clips['t2'].apply(lambda x : timestamp_to_seconds(x)).to_numpy()
    else:
        mint2_mask = np.ones(n).astype(bool)
        
    if args.max_t2 != np.inf:
        maxt2_mask = clips['t2'].apply(lambda x : timestamp_to_seconds(x)).to_numpy() <= args.max_t2
    else:
        maxt2_mask = np.ones(n).astype(bool)
    
    if args.include_placeholder:
        #We should include placeholders.
        placeholder_mask = np.ones(n).astype(bool)
    else:
        #Only keep clips where the name is not "placeholder".
        placeholder_mask = clips['name'].str.lower() != 'placeholder'
    
    
    if args.no_prefix:
        prefix = ''
    else:
        prefix = clips['tag']+'_C'+clips['nclip'].astype(str).str.zfill(2)+'_R'+clips['rating'].astype(str).str.zfill(2)+'_'
    
    #Stitch together the pathout.
    clips['pathout'] = ('./export/'+prefix+clips['name']+'.'+args.file_type)
    
    #Combine all of the masks into a final single mask, and cut out the relevant clips.
    final_mask = (clipname_mask) & (minrating_mask) & (maxrating_mask) & (minduration_mask) & (maxduration_mask) & (tags_mask)\
                 & (mint1_mask) & (maxt1_mask) & (mint2_mask) & (maxt2_mask) & (placeholder_mask)
    
    clips_final = clips.copy().loc[final_mask]
    
    #Check if there are any clips.
    if len(clips_final) == 0:
        if not np.any(clipname_mask):
            print('There are no clips with the specified name.')
            close_match = difflib.get_close_matches(args.clip_name, list(clips['name']))
            if close_match != []:
                print(f'Did you perhaps mean {close_match}?')
        else:
            print('No clips met the specified query.')
        return
    

    n = len(clips_final)
    
    if not args.silent:
        bom1.print_clips(clips_final)
        
    #If we pass the --list args, then it should only print.
    if args.list:
        return

    if n > 1:
        print('')
        prompt = input(f'A total of {n} clips were found. Do you want to export as {args.file_type}? [y/n] ').lower().strip() #Ask for confirmation if several clips are exported.
        print('')
    else:
        prompt = input(f'A single clip was found. Do you want to export as {args.file_type}? [y/n] ').lower().strip() #Ask for confirmation if several clips are exported.
        print('')

    if (prompt != 'y') and (prompt != ''):
        return
    
    #Start time before clipping.
    start_time = time.time()
    
    #Call to the clipper.
    bom1.clip(clips_final['t1'].tolist(), clips_final['t2'].tolist(), clips_final['link'].tolist(), clips_final['pathout'], args)

    end_time = time.time()
    print('')
    print("Time elapsed: {:.2f} seconds.".format(end_time-start_time))

                
if __name__ == '__main__':
    main()