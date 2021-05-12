
# Best of Mat 1

![bom1](https://user-images.githubusercontent.com/35364024/115997115-2d87d280-a5e2-11eb-867a-d1796633f8a0.gif)

## An Even Better Story... ⏳

In the summer of 2018, my friend Rasmus Aagaard ([@rasgaard](https://github.com/rasgaard)) and I enjoyed watching Advanced Engineering Mathematics 1 lectures by Michael Pedersen for fun. I had just finished the course and rewatched the lectures for fun, while Rasmus had finished the course the year before albeit with a different lecturer.

After having watched a few lectures, we decided to use my computer and iMovie to download the lectures, mark Michael's jokes and clip them out. After a while, we had watched about 5 or 10 lectures and had a decent compilation of clips and jokes. 

### Best of Mat 1 (2017/2018)

After having realized that a lot of friends and family found the clips to be rather funny, I decided to spend much of my summer holiday to rewatch the entirety of Advanced Engineering Mathematics 1 (fall semester of 2017 and spring semester of 2018). This, of course, took quite a while. While I haven't exactly calculated how many hours I spent watching lectures and clipping it together in iMovie, I know that it was probably at least **150 hours** just from watching, pausing, clipping and so on. 

This way of clipping had *many* flaws, but the three biggest, as I see it, were:

First of all, it was very hard on my poor MacBook. Since I clipped it all in a single iMovie project, sometimes iMovie would crash and I would be scared that I had lost all of my progress. Luckily, that did not happen and iMovie decided to pull through. (most of the time, atleast...)

Secondly, since I worked on a local project, no one were able to help out with the clipping, since all of the files were on my computer. This means that while some of my friends wanted to help by watching a lecture, it would be difficult to share their findings over to my system without me having to watch the lectures and manually cliping it out again. 

Thirdly, and perhaps the biggest problem, was that I had no system of labeling the clips or rating them. In the end, I had boiled all of the lectures down to **3.5 hours** of funny moments and jokes. But even then, some jokes were funnier than others, so if I had to shorten it even further down, I had to watch 3.5 hours of jokes to find the funniest... and after watching 3.5 hours of jokes, it's very hard to determine if something is fun or not. 

Nevertheless, me and some friends threw together [Best of Mat 1-event](https://www.facebook.com/events/459509117872655/), where we filled up DTU's biggest auditorium at the time and had 637 attendees on Facebook. None of us expected that **that** many people would show up to watch highlights. Originally, we figured some 30 people would join in Kælderbaren, but the event grew totally out of proportions. 

https://user-images.githubusercontent.com/35364024/115996963-a2a6d800-a5e1-11eb-805e-a1b2ab71e45b.mov


After the event, I realized that if I was ever to remake the event, I had to have some way of cutting it even further down since that for most normal people, 3.5 hours was too long, and that perhaps, 2 x 30 minutes would be more fitting. After the event, I went back to iMovie and clipped the 3.5 hours further down to what is today [Best of Mat 1 - 2017/2018](https://www.youtube.com/watch?v=vr192nWESRA). 

### Best of Mat 1 (2018/2019)

The next summer, I knew that my solution had to deal with the three problems I had the year before:

1. My solution should not be dependent on iMovie.
2. My solution should allow for others to join in on the clipping.
3. My solution should provide overview of which clips I had, their duration and how funny they were.

Therefore, I came up with the idea of having a so-called "Klippeark" for each lecture, in which I simply put in information about the different clips. 

| t1    | t2    | name                   | rating |
| :--   | :--   | :-:                    | :-:    |
| 00:03 | 00:11 | Fredag i skyttegravene | 7      |
| 00:30 | 00:43 | ReducedRowEchelonForm  | 8      |
| 01:50 | 02:02 | Vagthunden og Maple    | 6      |

Then, the main idea was to download all of the lectures and let my clipping script do the clipping. Then, I could just select my favourite clips and do some fine trimming such that I had 2 x 30 minutes. My new system worked pretty much perfectly! There was only one flaw, and that was that while I sent out the "Klippeark" to friends, I had watched most of the lectures before they even got around to watching them... but I mean, with the ease of clipping that my new system provided, it was a joy to watch Michael's new lectures (which I had not seen before). [Best of Mat 1 - 2018/2019](https://www.facebook.com/events/362771311018272/) turned out to be a great success. Michael once again attended the event and like the previous year, we gave him some flowers and a big basket filled with various wines, chocolate and beer.

<img src="https://user-images.githubusercontent.com/35364024/118003790-2c2c0900-b349-11eb-9c83-261dfed54eb3.png" width="500" height="500">

## Installation and Setup 🛠️

1. Download the repository from GitHub by writing ``git clone https://github.com/vstenby/Best-of-Mat-1.git`` in your terminal.

2. Make sure you have ``ffmpeg`` installed. 

3. Before you run anything, check that your folder structure is like this:

```
.
├── LICENSE
├── README.md
├── bom1.py
├── csv
└── main.py
 ```

4. Once this is done, run the script by: ``python main.py``

## Optional Arguments and How to Use Them

Note that this script has many different options that you can play around with to get the specific clips you want and in the format that you want them. You can always check which options are available by typing ``python main.py --help`` in the terminal.

```
python main.py --help

      ____            _            __   __  __       _     __ 
     |  _ \          | |          / _| |  \/  |     | |   /_ |
     | |_) | ___  ___| |_    ___ | |_  | \  / | __ _| |_   | |
     |  _ < / _ \/ __| __|  / _ \|  _| | |\/| |/ _` | __|  | |
     | |_) |  __/\__ \ |_  | (_) | |   | |  | | (_| | |_   | |
     |____/ \___||___/\__|  \___/|_|   |_|  |_|\__,_|\__|  |_|
        
             Best of Mat 1: Release 2.1.0 (24/04/2021)        

Author: Viktor Stenby Johansson
If you have any problems with this software, feel free to reach out to me via Facebook.

usage: main.py [-h] [--list] [--clipname CLIPNAME]
               [--minrating {1,2,3,4,5,6,7,8,9,10}]
               [--maxrating {1,2,3,4,5,6,7,8,9,10}]
               [--minduration MINDURATION] [--maxduration MAXDURATION]
               [--tag TAG] [--mint1 MINT1] [--maxt1 MAXT1] [--mint2 MINT2]
               [--maxt2 MAXT2] [--filetype {mp3,mp4}] [--normalizeaudio]
               [--noprefix] [--clearexport] [--silent]

optional arguments:
  -h, --help            show this help message and exit
  --list                print the list of clips instead of actually exporting
                        them.
  --clipname CLIPNAME   specify which clip name you want to export.
  --minrating {1,2,3,4,5,6,7,8,9,10}
                        only export clips with rating >= minrating.
  --maxrating {1,2,3,4,5,6,7,8,9,10}
                        only export clips with rating <= maxrating.
  --minduration MINDURATION
                        only export clips with duration >= minduration.
                        duration is in seconds.
  --maxduration MAXDURATION
                        only export clips with duration <= maxduration.
                        duration is in seconds.
  --tag TAG             regex for specfiying which tag you want to export.
  --mint1 MINT1         only export clips with mint1 <= t1.
  --maxt1 MAXT1         only export clips with t1 <= maxt1.
  --mint2 MINT2         only export clips with mint2 <= t2.
  --maxt2 MAXT2         only export clips with t2 <= maxt2.
  --filetype {mp3,mp4}  filetype to export as either mp3 or mp4.
  --normalizeaudio      normalize the audio of the output clip, which will
                        make the clipper take longer. this only works with mp4
                        at the moment.
  --noprefix            include prefix specifying info about the clip.
  --clearexport         clear the export folder before exporting.
  --silent              if --silent is passed, then progress is not printed to
                        the console.
```

### Examples Using Optional Arguments

| What You Want    | How You Do It
| :-:              | :-:   |
| List all clips   | ``python main.py --list`` |
| Export all clips as mp3 | ``python main.py`` | 
| Export all clips as mp4 | ``python main.py --filetype 'mp4' ``|
| Export clips with rating 8 or above | ``python main.py --minrating 8 ``|
| Export clips with rating 10 as mp4  | ``python main.py --minrating 10 --filetype 'mp4'``|
| Export clips shorter than 30 seconds | ``python main.py --maxduration 30 ``|
| Export clips from E19 | ``python main.py --tag E19* ``|
| Export clips from the first 60 seconds of all lectures (e.g. "Godmorgen"-clips) | ``python main.py --maxt1 60``|


If you have any ideas for useful optional arguments, please feel free to reach out to me or request a feature [here](https://github.com/vstenby/Best-of-Mat-1/issues).

## Special Thanks 🙏

I would like to thank Jonas ([@YoonAddicting](https://github.com/YoonAddicting/DTU-Video-Downloader)) for his DTU-Video-Downloader. Without his downloader, Best of Mat 1 would not have happend after DTU changed over to video.dtu.dk. 

Furthermore, I would also like to thank Rasmus ([@rasgaard](https://github.com/rasgaard)) for many lively discussions on the software and for many hours of watching lectures. 

Finally, I would like to thank Michael Pedersen. Michael has always been very understanding about the project and understood that it is done out of love to his work  as DTU's best lecturer and his wholesome person. 
