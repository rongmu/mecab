#!/usr/bin/env python2
# coding: utf-8
from __future__ import print_function
import os, sys, codecs
import cPickle as pickle

pickled_sentences  = os.path.join(os.path.dirname(__file__),
              os.path.normpath("data/pickled_sentences.txt"))

sentences = pickle.load(open(pickled_sentences, "rb"))

counter_report_brief = os.path.join(os.path.dirname(__file__),
              os.path.normpath("data/counter_report_brief.txt")) 
counter_report_detail = os.path.join(os.path.dirname(__file__),
              os.path.normpath("data/counter_report_detail.txt")) 

total_verb_amount = 0
total_counter_amount = 0
counters = []
verbs = []

def collect_nodes(node, list):
    for element in list:
        if element["name"] == node.primary_form:
            element["nodes"].append(node)
            return

    element_new = {"name": node.primary_form, "nodes": [node]}
    list.append(element_new)

def sort_list(list):
    return sorted(list, key = lambda e: len(e["nodes"]),
                            reverse = True)

def counters_report_brief(out = sys.stdout):
    print(u"# 助数詞の数：%d, 総度数: %d" % (len(counters), total_counter_amount), file = out)
    print(u"助数詞\t度数\t相対度数", file = out)

    for e in counters:
        print(e["name"],
              len(e["nodes"]),
              "{:.2%}".format(len(e["nodes"])/float(total_counter_amount)),
              sep = "\t", file = out)

def counters_report_detail(out = sys.stdout):
    print(u"助数詞の数：%d, 総度数: %d" % (len(counters), total_counter_amount), file = out)
    print("=" * 35 + "\n", file = out)

    counter_count = 0
    for counter in counters:
        counter_count += 1
        co_verbs = []

        print(u"#{:d} 助数詞：{}, 度数：{:d}, 相対度数：{:.2%} ".format(counter_count, counter["name"], len(counter["nodes"]), len(counter["nodes"])/float(total_counter_amount)), file = out)

        for e in counter["nodes"]:
            collect_nodes(e.next, co_verbs)

        print(file = out)
        print(u"共起する動詞の数：%d\n" % len(co_verbs), file = out)

        verb_count = 0
        for verb in sort_list(co_verbs):
            verb_count += 1
            print(u"{:d}. 動詞：{}, 度数：{:d}, 相対度数：{:.2%}, 文： ".format(verb_count, verb["name"], len(verb["nodes"]), len(verb["nodes"])/float(len(counter["nodes"]))), file = out)

            sentence_count = 0
            for node in verb["nodes"]:
                sentence_count += 1
                print(u"({:d}) {}".format(sentence_count,
                    node.sentence.raw), file = out)

            print( file = out )

        print("\n" + "=" * 35 + "\n", file = out)


def verbs_report_brief():
    print(u"# 動詞の数：%d, 総度数: %d" % (len(verbs), total_verb_amount))
    print(u"動詞\t度数\t相対度数")
    for e in verbs:
        print(e["name"],
              len(e["nodes"]),
              "{:.2%}".format(len(e["nodes"])/float(total_verb_amount)),
              sep = "\t")

# main
for sentence in sentences:
    for node in sentence.separated_numerals:
        total_verb_amount += 1
        collect_nodes(node.next, verbs)

        if node.class_detail2 == u"助数詞":
            total_counter_amount += 1
            collect_nodes(node, counters)

counters = sort_list(counters)
verbs = sort_list(verbs)

counters_report_brief(codecs.open(counter_report_brief, "w", "sjis"))
counters_report_detail(codecs.open(counter_report_detail, "w", "sjis"))
