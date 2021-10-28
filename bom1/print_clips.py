import pandas as pd

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