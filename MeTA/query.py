#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/19 3:26 PM

@author: Tangrizzly
"""

import metapy
import pickle
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--query', default='information retrieval', help='query keywords')
opt = parser.parse_args()

# todo: add user feedback as relevance judgments

start = time.time()
inv_idx = metapy.index.make_inverted_index('inv_id_config.toml')
end = time.time()
print(end - start)

print('num_docs: %d, unique_terms: %d, avg_doc_length: %d, total_corpus_terms: %d' %
      (inv_idx.num_docs(), inv_idx.unique_terms(), inv_idx.avg_doc_length(), inv_idx.total_corpus_terms()))

ranker = metapy.index.OkapiBM25()

query = metapy.index.Document()
query.content(opt.query)

top_docs = ranker.score(inv_idx, query, num_results=20)

with open('titles', 'rb') as f:
    titles = pickle.load(f)
with open('introductions', 'rb') as f:
    introductions = pickle.load(f)
with open('filelist', 'rb') as f:
    filelist = pickle.load(f)

for (d_id, _) in top_docs:
    print("link: %s, title: %s, abstract: %s" % (filelist[d_id], titles[d_id], introductions[d_id]))
