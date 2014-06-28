#!/usr/bin/env python
# coding: utf-8

import MeCab, codecs, os, platform

mecab_code = "utf-8" if not platform.system() == "Windows" else "sjis"

data_in  = os.path.join(os.path.dirname(__file__), 
                   os.path.normpath("../data/data_sentences.txt"))

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
t = MeCab.Tagger()

f_in = codecs.open(data_in, "r", "sjis")

count = 0

for line in f_in:
    if count >= 5: break
    count += 1

    # run t.parse() onece!
    res = t.parse(line.encode(mecab_code)).decode(mecab_code)

    # print res
    print "EOS"

    node = t.parseToNode(line.encode(mecab_code))
    node = node.next

    while node.next:
        surface = node.surface
        feature = node.feature
        print surface, "\t", feature

        # node_info = extract_feature(node.feature.decode(mecab_code))
        # node_info.update({ "surface": surface} )

        node = node.next

    # with codecs.open(os.path.join(os.path.dirname(__file__), 
    #         os.path.normpath('python-mecab-encoding-test')), 'a', 'sjis') \
    #         as f:
    #     f.write(res)
