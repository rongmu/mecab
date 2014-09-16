#!/usr/bin/python2
# -*- coding: utf-8 -*-
import MeCab, sys, string

features = ["hinshi",
            "saibun1",
            "saibun2",
            "saibun3",
            "katsuyou",
            "katsuyougata",
            "genkei",
            "yomi",
            "hatsuon"]

def extract_feature(csv):
    result = {}

    for k, v in zip(features, csv.split(",")):
        result[k] = v

    return result

# main
sentence = u"俺を倒すには百万年も早いぞ！".encode('shift-jis')

try:

    print "MeCab Version is %s" % (MeCab.VERSION,)

    t = MeCab.Tagger(" ".join(sys.argv))

    print t.parse(sentence)

    m = t.parseToNode(sentence)
    m = m.next
    while m.next:
        f = extract_feature(m.feature)

        if f["saibun1"] == u"数".encode('shift-jis'): 
            print m.surface, "\t", m.feature
        m = m.next
    print "EOS", "\n"

except RuntimeError, e:
    print "RuntimeError:", e;
