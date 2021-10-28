from .timestamp_to_seconds import *
from .seconds_to_timestamp import *
from .fix_outpath import *
from .parser import *
from .fetch_ID import *
from .stream_link import *
import subprocess

import queue
import threading

def ffmpeg_clip(t1, duration, url, outpath, args, n = None):
    '''
    Export a clip.
    Input:
        t1:        start time (timestamp)
        duration:  duration   (timestamp)
        url:       stream link
    '''
    
    
    if outpath.endswith('.mp3') or outpath.endswith('.wav'):
        bashcmd = f'ffmpeg -y -ss {t1} -i "{url}" -t {duration} -ar {args.ar} -q:a 0 -map a {outpath} -loglevel error'
    elif outpath.endswith('.mp4') or outpath.endswith('.gif'):
        bashcmd = f'ffmpeg -y -ss {t1} -i "{url}" -t {duration} {outpath} -ar {args.ar} -loglevel error -ar {ar}'
    else:
        raise ValueError('Wrong output format.')
            
    rtrn = subprocess.call(bashcmd, shell=True)
    
    assert rtrn == 0, 'Download failed.'
        
    
    if args.normalize and outpath.endswith('.mp4'):
        #This might fail if you don't have ffmpeg-normalize installed. pip3 install ffmpeg-normalize. Normalization also only seems to work with mp4.
        normalize_rtrn = subprocess.call(f'ffmpeg-normalize {outpath} -o {outpath} -c:a aac -b:a 192k -f', shell=True, 
                                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
    if not args.silent:
        global count
        count += 1
        if not rtrn:
            print((str(count)+'/'+str(n)).ljust(9) + f'{outpath} succesfully exported.')
        else:
            print((str(count)+'/'+str(n)).ljust(9) + f'{outpath} was not exported exported.')
        
    return rtrn

#worker threads for queues
def workerThread(q):
    while True:
        args = q.get()[0:]
        ffmpeg_clip(*args)
        q.task_done()

    return

def clip(t1, t2, url, outpath, args = parser().parse_args([]),
        #Here, we set all arguments that can be used by ffmpeg_clip. 
        prepad    = None, 
        postpad   = None,
        normalize = None,
        silent    = None,
        threads   = None,
        ar        = None,
        ):
    
    if prepad is not None:    args.prepad = prepad
    if postpad is not None:   args.postpad = postpad
    if normalize is not None: args.normalize = normalize
    if silent is not None:    args.silent = silent
    if threads is not None:   args.threads = threads
    if ar is not None:        args.ar = ar
    
    
    #Make sure that all arguments are good to go.
    outpath  = [fix_outpath(x) for x in outpath]
    url      = [stream_link(fetch_ID(x)) for x in url]
    t1       = [seconds_to_timestamp(x) for x in t1] #make sure all t1 are timestamps.
    t2       = [timestamp_to_seconds(x) for x in t2]  #make sure all t2 are seconds.
    duration = [seconds_to_timestamp(y - timestamp_to_seconds(x)) for x, y in zip(t1, t2)] #This will fail if t1 and t2 have different lengths.
        
    #Set the count for exporting in parallel.
    global count
    count = 0
    
    q = queue.Queue(0)

    n = len(t1)
    
    for t1, duration, url, outpath in zip(t1, duration, url, outpath):
        q.put((t1,duration,url, outpath, args, n,))
        
    for _ in range(args.threads):
        worker = threading.Thread(target=workerThread, args=(q,))
        worker.setDaemon(True)
        worker.start()

    q.join()
    q = None
    
    return 