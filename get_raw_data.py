#!/usr/bin/env python
# coding: utf-8
import os, codecs, re
import time

start_time = time.time()

echo = False # echo qualified lines or not
# total amount of qualified lines, float("inf") is infinite.
max_count = float("inf")

count = 0
line_num = 0

dir_path = os.path.dirname(__file__)
file_in  = os.path.join(dir_path, os.path.normpath(
            ur"mainichi-corpus/2010年毎日新聞コーパス/mai2010.txt")) 
file_out = os.path.join(dir_path, 
                        os.path.normpath("data/data_raw.txt"))

content_tag = ur"^＼Ｔ２＼　*"
# qualified content lines should have at least one sentence.
content_pat = content_tag + ur".+[。！？]"

f_in  = codecs.open(file_in, "r", "shift-jis")
f_out = codecs.open(file_out, "w", "shift-jis")

for line in f_in:
    if count >= max_count: break
    line_num += 1

    if re.match(content_pat, line):
        count += 1
        content = re.sub(content_tag, "", line) 
        f_out.write(content)

        if echo == True:
            print "count:%d, line:%d: \n%s" % \
                  (count, line_num, content)

f_in.close()
f_out.close()

print "elapsed_time:", time.time() - start_time
