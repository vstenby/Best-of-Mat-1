# Best of Mat 1

## About

In the summer of 2018, my friend Rasmus Aagaard ([@rasgaard](https://github.com/rasgaard)) and I enjoyed watching Advanced Engineering Mathematics 1 lectures by Michael Pedersen for fun. I had just finished the course and rewatched the lectures for fun, while Rasmus had finished the course the year before albeit with a different lecturer.

After having watched a few lectures, we decided to use my computer and iMovie to download the lectures, mark Michael's jokes and clip them out. After a while, we had watched about 5 or 10 lectures and had a decent compilation of clips and jokes. 

### Best of Mat 1 (2017/2018)

After having realized that a lot of friends and family found the clips to be rather funny, I decided to spend much of my summer holiday to rewatch the entirety of Advanced Engineering Mathematics 1 (fall semester of 2017 and spring semester of 2018). This, of course, took quite a while. While I haven't exactly calculated how many hours I spent watching lectures and clipping it together in iMovie, I know that it was probably at least **150 hours** just from watching, pausing, clipping and so on. 

This way of clipping had *many* flaws, but the three biggest, as I see it, were:

First of all, it was very hard on my poor MacBook. Since I clipped it all in a single iMovie project, sometimes iMovie would crash and I would be scared that I had lost all of my progress. Luckily, that did not happen and iMovie decided to pull through. (most of the time, atleast...)

Secondly, since I worked on a local project, no one were able to help out with the clipping, since all of the files were on my computer. This means that while some of my friends wanted to help by watching a lecture, it would be difficult to share their findings over to my system without me having to watch the lectures and manually cliping it out again. 

Thirdly, and perhaps the biggest problem, was that I had no system of labeling the clips or rating them. In the end, I had boiled all of the lectures down to **3.5 hours** of funny moments and jokes. But even then, some jokes were funnier than others, so if I had to shorten it even further down, I had to watch 3.5 hours of jokes to find the funniest... and after watching 3.5 hours of jokes, it's very hard to determine if something is fun or not. 

Nevertheless, me and some friends threw together [Best of Mat 1-event](https://www.facebook.com/events/459509117872655/), where we filled up DTU's biggest auditorium at the time and had 637 attendees on Facebook. None of us expected that **that** many people would show up to watch highlights. Originally, we figured some 30 people would join in Kælderbaren, but the event grew totally out of proportions. After the event, I realized that if I was ever to remake the event, I had to have some way of cutting it even further down since that for most normal people, 3.5 hours was too long, and that perhaps, 2 x 30 minutes would be more fitting. After the event, I went back to iMovie and clipped the 3.5 hours further down to what is today [Best of Mat 1 - 2017/2018](https://www.youtube.com/watch?v=vr192nWESRA). 

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

## Installation and Setup

1. Download the repository from GitHub by writing ``git clone --recursive https://github.com/vstenby/Best-of-Mat-1.git`` in your terminal.

2. Make sure that you have the following Python packages installed:

    * ``moviepy`` for clipping.
    * ``selenium`` for downloading the lectures from [video.dtu.dk](video.dtu.dk)
    
3. Download the appropriate chromedriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

4. Check your folder setup. It should be as follows:

```
.
├── DTU-Video-Downloader
│   ├── DTU_VD_functions.py
│   ├── LICENSE
│   ├── README.md
│   └── main.py
├── LICENSE
├── README.md
├── bom1.py
├── chromedriver
├── main.py
├── settings.py
└── tsv
    ├── E18_B
    ├── E19_B
    └── F19_B 
 ```

5. Once this is done, run the script by: ``python main.py``

In the ``settings.py``, you can change the outputtype to either ``.mp3`` or ``.mp4``, depending on if you want to export the clips as audio or video. You can also specify if you want clips that are of a shorter duration, or if you want only clips with a specific rating.  

## Feature Overview

Here, I have listed some features that I would like to work on in the future. 

### Current Features
- [x] User can specify export format (.mp3 or .mp4)
- [x] User can specify minimum rating
- [x] User can specify minimum duration

### Future Features

- [ ] Easy overview for user of available clips.
- [ ] Export specific clip(s), i.e. by name, lecture, semester ... 
- [ ] Google Chrome Extension such that users can easily add more clips. 

Please feel free to add suggestions for features [here](https://github.com/vstenby/Best-of-Mat-1/issues).

## Special Thanks

I would like to thank Jonas ([@YoonAddicting](https://github.com/YoonAddicting/DTU-Video-Downloader)) for his DTU-Video-Downloader. Without his downloader, Best of Mat 1 would not have happend after DTU changed over to video.dtu.dk. 

Furthermore, I would also like to thank Rasmus ([@rasgaard](https://github.com/rasgaard)) for many lively discussions on the software and for many hours of watching lectures. 

Finally, I would like to thank Michael Pedersen. Michael has always been very understanding about the project and understood that it is done out of love to his work  as DTU's best lecturer and his wholesome person. 
