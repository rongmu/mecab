#!/usr/bin/env python2
# coding: utf-8
import MeCab, platform

mecab_code = "utf-8" if not platform.system() == "Windows" else "sjis"

class Node:
    feature_list = ["word_class",
                    "class_detail1",
                    "class_detail2",
                    "class_detail3",
                    "conjugation_type",
                    "conjugation_form",
                    "primary_form",
                    "kana_notation",
                    "pronunciation"]

    def __init__(self, sentence, index, surface, features):
        self.sentence = sentence
        self.index = index

        # nodes will be linked later by Sentence.link_nodes().
        self.prev = None
        self.next = None

        self.surface = surface
        self.set_features(features)

    def __str__(self):
        return self.surface.encode(mecab_code)

    def set_features(self, features_csv):
        for feature, value in \
                zip(Node.feature_list, features_csv.split(",")):
            setattr(self, feature, value)

class Sentence:
    tagger = MeCab.Tagger()
    tagger.parse(u"こんにちは、めかぶ".encode(mecab_code))

    def __init__(self, raw_sentence):
        self.raw = raw_sentence
        self.nodes = []
        self.nodes_size = 0

        self.parse()

    def __str__(self):
        return self.raw.encode(mecab_code)

    def parse(self):
        self.nodes = []

        raw_encoded = self.raw.encode(mecab_code)

        node_mecab = Sentence.tagger.parseToNode(raw_encoded)
        node_mecab = node_mecab.next

        node_index = 0

        while node_mecab.next:
            surface = node_mecab.surface.decode(mecab_code)
            feature = node_mecab.feature.decode(mecab_code)

            node = Node(self, node_index, surface, feature)
            self.nodes.append(node)

            node_index += 1
            node_mecab = node_mecab.next

        self.nodes_size = len(self.nodes)

        self.link_nodes()

    def link_nodes(self):
        for node in self.nodes:
            if not node.index == 0:
                node.prev = self.nodes[node.index - 1]
            if not node.index == (self.nodes_size - 1):
                node.next = self.nodes[node.index + 1]

    def find(self, str):
        result = None

        for node in self.nodes:
            if node.surface == str:
                result = node
                break

        return result


if __name__ == '__main__':
    import sys

    s = Sentence(u"私は日本語を勉強しています。")

    print s.raw
    
    res  = s.find(u"勉強")
    print res.prev, res, res.next
