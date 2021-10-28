def fix_outpath(path):
    '''
    Fixes the path out by removing letters that cause issues when exporting.
    '''
    pathout = path.replace(' ','_')\
                  .replace(',','')\
                  .replace("'","")\
                  .replace(')','').replace('(','')
    
    return pathout