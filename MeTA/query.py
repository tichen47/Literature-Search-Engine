#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/19 3:26 PM

@author: Tangrizzly
"""
import argparse
import metapy
import pickle
import time
from ranker import SimpleRanker, Jelinek_Mercer, Absolute_Discount, DirichletPrior

def search(input):
    # todo: add user feedback as relevance judgments

    parser = argparse.ArgumentParser()
    parser.add_argument('--query', default='information retrieval', help='query keywords')
    opt = parser.parse_args()

    start = time.time()
    inv_idx = metapy.index.make_inverted_index('MeTA/inv_id_config.toml')
    end = time.time()
    print(end - start)

    print('num_docs: %d, unique_terms: %d, avg_doc_length: %d, total_corpus_terms: %d' %
        (inv_idx.num_docs(), inv_idx.unique_terms(), inv_idx.avg_doc_length(), inv_idx.total_corpus_terms()))

    doc_weight=None
    ranker = SimpleRanker(doc_weight, score_func='score_BM25_L')

    query_keywords = metapy.index.Document()
    query_keywords.content(opt.query)

    top_docs = ranker.score(inv_idx, query_keywords, num_results=20)

    with open('MeTA/titles', 'rb') as f:
        titles = pickle.load(f)
    with open('MeTA/introductions', 'rb') as f:
        introductions = pickle.load(f)
    with open('MeTA/filelist', 'rb') as f:
        filelist = pickle.load(f)

    ans = []
    for (d_id, _) in top_docs:
        fin = "https://www.aclweb.org/anthology/" + filelist[d_id].split(".")[0] + ".pdf"
        ans.append((fin, titles[d_id], introductions[d_id]))
    return ans


if __name__ == '__main__':
    ans = search('systems')
    pickle.dump(ans, open('results', 'wb'))
    print('dump ok!')