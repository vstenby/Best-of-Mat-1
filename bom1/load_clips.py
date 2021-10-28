import numpy as np
import pandas as pd
import os
from .duration import *
from .seconds_to_timestamp import *
from .timestamp_to_seconds import *

def load_clips(load_empty=False):
    
    #Define the reversor used to sort the csv.
    class reversor:
        def __init__(self, obj):
            self.obj = obj

        def __eq__(self, other):
            return other.obj == self.obj

        def __lt__(self, other):
            return other.obj < self.obj

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

    return clips