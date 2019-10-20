#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/19 3:26 PM

@author: Tangrizzly
"""
import metapy
import pickle
import time
<<<<<<< HEAD
=======
import os

def test(input):
    thislist = ["apple", "banana", "cherry", input]
    return thislist

def search(input):
    # parser = argparse.ArgumentParser()
    # parser.add_argument(input, default='information retrieval', help='query keywords')
    # opt = parser.parse_args()
>>>>>>> bd219652c5dbe28b8c284fcc2e4edf35fe60fb8b


def search(input):
    # todo: add user feedback as relevance judgments

    start = time.time()
<<<<<<< HEAD
=======
    #if not os.path.exists('inv_id_config.toml'):
    #    print('Not exist')
    #    exit(-1)

>>>>>>> bd219652c5dbe28b8c284fcc2e4edf35fe60fb8b
    inv_idx = metapy.index.make_inverted_index('MeTA/inv_id_config.toml')
    end = time.time()
    print(end - start)

    print('num_docs: %d, unique_terms: %d, avg_doc_length: %d, total_corpus_terms: %d' %
        (inv_idx.num_docs(), inv_idx.unique_terms(), inv_idx.avg_doc_length(), inv_idx.total_corpus_terms()))

    ranker = metapy.index.OkapiBM25()

    query = metapy.index.Document()
<<<<<<< HEAD
=======
    # query.content(opt.query)
>>>>>>> bd219652c5dbe28b8c284fcc2e4edf35fe60fb8b
    query.content(input)

    top_docs = ranker.score(inv_idx, query, num_results=20)

    with open('MeTA/titles', 'rb') as f:
        titles = pickle.load(f)
    with open('MeTA/introductions', 'rb') as f:
        introductions = pickle.load(f)
    with open('MeTA/filelist', 'rb') as f:
        filelist = pickle.load(f)

    ans = []
    for (d_id, _) in top_docs:
        ans.append((filelist[d_id]+titles[d_id]+introductions[d_id]))
        # print("link: %s, title: %s, abstract: %s" % (filelist[d_id], titles[d_id], introductions[d_id]))
    return ans

<<<<<<< HEAD

if __name__ == '__main__':
    print(search('systems'))
=======
if __name__ == '__main__':
    result = search("hello")
    for item in result:
        print(item)
>>>>>>> bd219652c5dbe28b8c284fcc2e4edf35fe60fb8b
