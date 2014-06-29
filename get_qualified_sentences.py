#!/usr/bin/env python2
# coding: utf-8
import codecs, os, time
import cPickle as pickle
from mecab_utils.sentence import *

start_time = time.time()

qualified_sentences = []

data_in  = os.path.join(os.path.dirname(__file__), 
                os.path.normpath("data/data_sentences.txt"))
data_out  = os.path.join(os.path.dirname(__file__), 
                os.path.normpath("data/pickled_sentences.txt"))

def has_numeral_separation(sentence):
    sentence.separated_numerals = []
    result = False

    for node in sentence.nodes:
        if ( node.class_detail2 == u"助数詞" and \
                node.next.word_class == u"動詞"
                ) or ( node.class_detail1 == u"数" and \
                       node.next.word_class == u"動詞" ):
            sentence.separated_numerals.append(node)
            result = True

    return result

with codecs.open(data_in, "r", "sjis") as f:
    for line in f:
        s = Sentence(line)
        if has_numeral_separation(s):
            qualified_sentences.append(s)

print "Total qualified sentences: %d" % len(qualified_sentences)

pickle.dump(qualified_sentences, open(data_out, "wb"), 2)

elapsed_time = time.time() - start_time
print "elapsed_time %f" % elapsed_time
