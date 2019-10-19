#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/18 11:13 PM

@author: Tangrizzly
"""

import os
import pickle

path = '../grobid_processed/'

contents, titles, abstracts, introductions = [], [], [], []
filelist = sorted(os.listdir(path))
for filename in filelist:
    content, abstract, introduction = "", "", ""
    with open(path + filename, 'r') as f:
        line = f.readline()
        while line != '<figcaptions>\n':
            content += line[:-1] + ' '
            line = f.readline()

        while line != '<title>\n':
            line = f.readline()
        titles.append(f.readline()[:-1])

        f.readline()
        line = f.readline()
        while line != '<introduction>\n':
            abstract += line[:-1] + ' '
            line = f.readline()

        line = f.readline()
        while line:
            introduction += line[:-1] + ' '
            line = f.readline()

    contents.append(content)
    abstracts.append(abstract)
    introductions.append(introduction)

pickle.dump(titles, open('titles', 'wb'))
pickle.dump(abstracts, open('abstractions', 'wb'))
pickle.dump(introductions, open('introductions', 'wb'))
pickle.dump(filelist, open('filelist', 'wb'))
if not os.path.exists('contents'):
    os.mkdir('contents')
with open('contents/contents.dat', 'w') as f:
    f.writelines("%s\n" % content for content in contents)