#!/usr/bin/env python2
# coding: utf-8
import codecs

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

def write_sentences(sentences_tagged, data_path):
    with codecs.open(data_path, "w", "sjis") as f:
        for sentence in sentences_tagged:
            for n in sentence:
                f.write(n["surface"])
                # sys.stdout.write(n["surface"])
                
            f.write("\n")
            # sys.stdout.write("\n\n")

def count_frequency(word, word_frequency):
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

def freq_stats(word_frequency, ):
    word_list = []

    for key in word_frequency:
        word_list.append({'word': key, 'freq': word_frequency[key]})

    for e in sorted(word_list, key = lambda e: e['freq'], reverse = True):
        print e['word'], "\t", e['freq']

