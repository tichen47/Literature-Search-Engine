#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/19 2:58 PM
@author: Tangrizzly
"""

# reference: https://meta-toolkit.org/search-tutorial.html

with open('contents/corpus.toml', 'w') as f:
    f.write('type = "line-corpus"\n')
    f.write('store-full-text = true\n')

config = """prefix = "./MeTA" # tells MeTA where to search for datasets
dataset = "Acontents" # a subfolder under the prefix directory
corpus = "corpus.toml" # a configuration file for the corpus specifying its format & additional args
# query-judgements = "./MeTA/judgements.txt" # file containing the relevance judgments for this dataset
# [queryid docid relevance]
index = "./MeTA/contents-idx" # subfolder of the current working directory to place index files
stop-words = "./MeTA/stopwords.txt"
[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
"""

with open('inv_id_config.toml', 'w') as f:
    f.write(config)