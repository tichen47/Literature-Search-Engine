#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/12/11 2:16 PM

@author: Tangrizzly
"""
import json
import os
import pickle

dataset_path = 'dataset'
output_path = 'net_aminer'


def save_dict(_dict, type):
    list = []
    for k, v in _dict.items():
        if type == 'id_author':
            k = 'a' + k.replace(' ', '')
        elif type == 'id_conf':
            k = 'v' + k.replace(' ', '')
        list.append([v, k])
    with open(output_path + '/' + type + '.txt', 'w') as f:
        f.writelines('%s\t%s\n' % (l[0], l[1]) for l in list)


def save_rel(_rel, type):
    with open(output_path + '/' + type + '.txt', 'w') as f:
        f.writelines('%s\t%s\n' % (l[0], l[1]) for l in _rel)


if __name__ == '__main__':
    paper_dict = {}
    author_dict = {}
    conf_dict = {}
    p_c_rel = []
    p_a_rel = []
    details = []
    titles = []
    keywords = []
    docs = []

    for (dirpath, dirnames, filenames) in os.walk(dataset_path):
        for filename in filenames:
            if filename.endswith('.txt'):
                print(dirpath + '/' + filename)
                with open(dirpath + '/' + filename, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    obj = json.loads(line)
                    if 'abstract' not in obj or 'keywords' not in obj \
                            or 'url' not in obj or 'venue' not in obj or 'authors' not in obj:
                        continue
                    paper_dict[obj['title']] = len(paper_dict)
                    doc = obj['title'] + ' ' + obj['abstract'] + ' ' + ' '.join(obj['keywords'])
                    docs.append(doc)

                    if obj['venue'] not in conf_dict:
                        conf_dict[obj['venue']] = len(conf_dict)
                    p_c_rel.append([paper_dict[obj['title']], conf_dict[obj['venue']]])
                    obj['authors'] = [i['name'] for i in obj['authors']]
                    for author in obj['authors']:
                        if author is None:
                            continue
                        if author not in author_dict:
                            author_dict[author] = len(author_dict)
                        p_a_rel.append([paper_dict[obj['title']], author_dict[author]])
                    details.append([obj['title'], obj['authors'], obj['venue'], obj['url'][0]])

    with open('docs.txt', 'w') as f:
        f.writelines('%s\n' % line for line in docs)
    save_dict(conf_dict, 'id_conf')
    save_dict(author_dict, 'id_author')
    save_dict(paper_dict, 'paper')
    save_rel(p_c_rel, 'paper_conf')
    save_rel(p_a_rel, 'paper_author')
    pickle.dump(details, open('details', 'wb'))