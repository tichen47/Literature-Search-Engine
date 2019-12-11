#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/12/11 2:16 PM

@author: Tangrizzly
"""
import json
import os

dataset_path = 'dataset'

paper_dict = {}
author_dict = {}
conf_dict = {}
p_c_rel = []
p_a_rel = []

titles = []
keywords = []
abstracts = []

for (dirpath, dirnames, filenames) in os.walk(dataset_path):
    for filename in filenames:
        if filename.endswith('.txt'):
            print(dirpath + '/' + filename)
            with open(dirpath + '/' + filename, 'r') as f:
                lines = f.readlines()
            for line in lines:
                obj = json.loads(line)
                paper_dict['id'] = len(paper_dict)
                titles.append(obj['titles'])
                keywords.append(obj['keywords'])
                abstracts.append(obj['abstract'])
                if obj['vanue'] not in conf_dict:
                    conf_dict['vanue'] = len(conf_dict)
                p_c_rel.append([paper_dict['id'], conf_dict['vanue']])
                for author in obj['authors']:
                    if author['name'] not in author_dict:
                        author_dict[author] = len(author_dict)
                    p_a_rel.append([paper_dict['id'], author_dict[author]])


