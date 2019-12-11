#!/usr/bin/env python36
# -*- coding: utf-8 -*-
"""
Created on 2019/10/23 8:43 PM

@author: Tangrizzly
"""
import metapy
import math
import numpy as np

# reference: http://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf


class SimpleRanker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """

    def __init__(self, doc_weight, score_func='score_BM25_L'):
        self.ls = doc_weight
        self.score_func = score_func
        
        # You *must* invoke the base class __init__() here!
        super(SimpleRanker, self).__init__()

    def score_one(self, sd):
        k1 = 1.2
        k3 = 500
        b = 0.75
        delta = 0.5
        tf = sd.doc_term_count
        df = sd.doc_count
        idf = sd.num_docs / df
        if self.score_func == 'score_BM25':
            score = self.score_BM25(tf, idf, k1, b, sd.doc_size, sd.avg_dl)
        elif self.score_func == 'score_BM25_ATIRE':
            score = self.score_BM25_ATIRE(tf, df, k1, b, sd.doc_size, sd.avg_dl, sd.num_docs)
        elif self.score_func == 'score_BM25_L':
            score = self.score_BM25_L(tf, df, k1, b, sd.doc_size, sd.avg_dl, sd.num_docs, delta)
        elif self.score_func == 'score_BM25_L_Weight':
             score = self.score_BM25_L_Weight(tf, df, k1, b, sd.doc_size, sd.avg_dl, sd.num_docs, delta, self.ls[sd.d_id])
        else:  # self.score_func == 'score_BM25_Okapi':
            score = self.score_BM25_Okapi(tf, df, k1, k3, b, sd.doc_size, sd.avg_dl, sd.num_docs, sd.doc_count)
        return score

    def score_BM25(self, tf, idf, k1, b, doc_length, avg_doc_length):
        rate = math.log(idf)
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_length / avg_doc_length)
        return rate * numerator / denominator

    def score_BM25_ATIRE(self, tf, df, k1, b, doc_length, avg_doc_length, num_doc):
        rate = math.log(num_doc / df)
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_length / avg_doc_length)
        return rate * numerator / denominator

    def score_BM25_L(self, tf, df, k1, b, doc_length, avg_doc_length, num_doc, delta):
        c_td = tf / (1 - b + b * (doc_length / avg_doc_length))
        rate = np.log((num_doc + 1) / (df + 0.5))
        numerator = (k1 + 1) * (c_td + delta)
        denominator = k1 + c_td + delta
        return rate * (numerator / denominator) 
    
    def score_BM25_L_Weight(self, tf, df, k1, b, doc_length, avg_doc_length, num_doc, delta, weight):
        c_td = tf / (1 - b + b * (doc_length / avg_doc_length))
        rate = np.log((num_doc + 1) / (df + 0.5))
        numerator = (k1 + 1) * (c_td + delta)
        denominator = k1 + c_td + delta
        return rate * (numerator / denominator + 8 * weight)  # 4287


    def score_BM25_Okapi(self, tf, df, k1, k3, b, doc_length, avg_doc_length, num_doc, doc_count):
        r = 0
        R = 0
        qtf = 1
        K = k1 * (1 - b + b * (doc_length / avg_doc_length))
        rate = math.log(((r + 0.5) / (R - r + 0.5)) / ((doc_count - r + 0.5)/(num_doc - doc_count - R + r + 0.5)))
        numerator = (k1 + 1) * tf * (k3 + 1) * qtf
        denominator = (K + tf) * (k3 + qtf)
        return rate * numerator / denominator


class DirichletPrior(metapy.index.LanguageModelRanker):
    def __init__(self, mu=2000):
        # small value such as 0.7 to increase academic proformance
        self.mu = mu
        super(DirichletPrior, self).__init__()

    def smoothed_prob(self, sd):
        p_wc = sd.corpus_term_count / sd.total_terms
        p_seen = (sd.doc_term_count + self.mu * p_wc) / (sd.doc_size + self.mu)
        return p_seen

    def doc_constant(self, sd):
        alpha_d = self.mu / (sd.doc_size + self.mu)
        return alpha_d


class Jelinek_Mercer(metapy.index.LanguageModelRanker):
    def __init__(self, lamb=0.7):
        self.lamb = lamb
        super(Jelinek_Mercer, self).__init__()

    def smoothed_prob(self, sd):
        p_wc = sd.corpus_term_count / sd.total_terms
        p_seen = (1 - self.lamb) * (sd.doc_term_count / sd.doc_size) + self.lamb * p_wc
        return p_seen

    def doc_constant(self, sd):
        alpha_d = self.lamb
        return alpha_d


class Absolute_Discount(metapy.index.LanguageModelRanker):
    def __init__(self, delta=0.7):
        self.delta = delta
        super(Absolute_Discount, self).__init__()

    def smoothed_prob(self, sd):
        p_wc = sd.corpus_term_count / sd.total_terms
        numerator = max(sd.doc_term_count - self.delta, 0)
        p_seen = numerator / sd.doc_size + self.delta * (sd.doc_unique_terms / sd.doc_size) * p_wc
        return p_seen

    def doc_constant(self, sd):
        alpha_d = self.delta * (sd.doc_unique_terms / sd.doc_size)
        return alpha_d