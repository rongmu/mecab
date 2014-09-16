#!/usr/bin/env python2
# coding: utf-8
import os, codecs, re
import time

start_time = time.time()

# TODO: 鉤括弧の引用文を一行にするかどうか。

dir_path = os.path.dirname(__file__)

data_raw       = os.path.join(dir_path, 
                    os.path.normpath("data/data_raw.txt"))
data_sentences = os.path.join(dir_path, 
                    os.path.normpath("data/data_sentences.txt"))

f_in  = codecs.open(data_raw, "r", "shift-jis")
f_out = codecs.open(data_sentences, "w", "shift-jis")

sentence_term = u"。！？▲"
sentence_pat = ur"[^%s].+?[%s]" % ((sentence_term,) * 2)

# count = 0
for line in f_in:
    # if count >= 5: break
    # count += 1
    res = re.findall(sentence_pat, line)
    for e in res: 
        f_out.write(e + "\n")
        # print e

f_in.close()
f_out.close()

print "elapsed_time:", time.time() - start_time
