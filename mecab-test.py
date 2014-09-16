#!/usr/bin/env python2
# coding: utf-8

import MeCab, codecs, os, platform, time
from mecab_utils.functions import *

mecab_code = "utf-8" if not platform.system() == "Windows" else "sjis"

start_time = time.time()

MAX_COUNT = float("inf")

# currently using small test data
data_in  = os.path.join(os.path.dirname(__file__), 
                   os.path.normpath("data-test/data_sentences.txt"))
data_out  = os.path.join(os.path.dirname(__file__), 
                   os.path.normpath("data-test/data_numeral.txt"))

sentences_tagged = []

verb_frequency = {}
josushi_frequency = {}

# main
try:
    f_in = codecs.open(data_in, "r", "sjis")

    t = MeCab.Tagger()

    # dummy statement.
    # it is very strange that if you don't run t.parse() once
    # then parseToNode() won't work properly.
    # mainly about encoding problems.
    t.parse(u"こんにちは".encode(mecab_code))

    count = 0
    for line in f_in:
        if count >= MAX_COUNT: break
        count += 1

        sentence_nodes = []

        node = t.parseToNode(line.encode(mecab_code))
        node = node.next

        while node.next:
            surface = node.surface.decode(mecab_code)
            feature = node.feature.decode(mecab_code)

            node_info = {}
            node_info["surface"] = surface
            node_info.update(extract_feature(feature))

            sentence_nodes.append(node_info)
            node = node.next

        # 遊離数量詞を含む文を特定してみる。
        # 時間や回数や距離を表す数量詞を排除する必要ある？
        for i in xrange(0, len(sentence_nodes)):
            if sentence_nodes[i]["saibun1"] == u"数" \
                    and sentence_nodes[i+1]["hinshi"] == u"動詞":
                count_frequency(sentence_nodes[i+1]["genkei"],
                        verb_frequency)
                sentences_tagged.append(sentence_nodes)
                break

            if sentence_nodes[i]["saibun2"] == u"助数詞" \
                    and sentence_nodes[i+1]["hinshi"] == u"動詞":
                count_frequency(sentence_nodes[i+1]["genkei"],
                        verb_frequency)
                count_frequency(sentence_nodes[i]["genkei"],
                        josushi_frequency)
                sentences_tagged.append(sentence_nodes)
                break

    write_sentences(sentences_tagged, data_out)
    print "amount of qualified sentences: %d" % len(sentences_tagged)

    print "verb frequency stats:"
    freq_stats(verb_frequency)

    print
    
    print "josushi frequency stats:"
    freq_stats(josushi_frequency)

except RuntimeError, e:
    print "RuntimeError:", e

finally:
    f_in.close()

print
print "elapsed_time:", time.time() - start_time
