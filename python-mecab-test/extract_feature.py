#!/usr/bin/env python2
# coding: utf-8

csv = "名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ"

features = ["hinshi",
            "saibun1",
            "saibun2",
            "saibun3",
            "katsuyou",
            "katsuyougata",
            "genkei",
            "yomi",
            "hatsuon"]

def extract_features(csv):
    result = {}
    for k, v in zip(features, csv.split(",")):
        result[k] = v
    return result

r = extract_features(csv)
print r["hatsuon"]
