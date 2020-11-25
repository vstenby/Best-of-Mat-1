#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Settings for Best of Mat 1 clipper
import numpy as np

# If you want to export all clips, the syntax is:
#
# 'clips' : 'all'
#
# If you want to export a single / multiple clips, do it like this:
#
# 'clips' : ['3 ledige tavler - helt forfærdeligt'] 
#
# or 
#
# 'clips' : ['3 ledige tavler - helt forfærdeligt', 'En klam udregning']
#
# If you want to export specific semesters, do it like this:
#
# 'semesters' : ['F19_B', 'E19_B']

settings = {'min_rating' : 1,
            'max_duration' : np.inf,
            'semesters' : 'all',
            'outputtype' : '.mp4',
            'clips' : 'all'}







