#!/usr/bin/env python2
# coding: utf-8
import os
import cPickle as pickle

pickled_sentences  = os.path.join(os.path.dirname(__file__), 
                os.path.normpath("data-test/pickled_sentences.txt"))

sentences = pickle.load(open(pickled_sentences, "rb"))

for s in sentences:
    print s.raw
