# -*- coding: utf-8 -*-
# @Time    : 2020/8/13-17:09
# @Author  : 贾志凯
# @File    : nroute.py
# @Software: win10  python3.6 PyCharm
# import re
# import  os
# import sys
# from math import log
# class Segment:
#     def __init__(self):
#         self.vocab = {}
#         self.max_word_len = 0
#         self.max_freq = 0
#         self.total_freq = 0
#         self.initialized = False
#         self.model= None
#
#     def init(self,vocab_path='dict/jiagu.dict', user_vocab='dict/user.dict',model_path='model/cws.model'):
#         self.load_vocab(os.path.join(os.path.dirname(__file__), vocab_path))
#         self.load_vocab(os.path.join(os.path.dirname(__file__), user_vocab))
#         self.model = Perceptron(os.path.join(os.path.dirname(__file__), model_path))
#         self.initialized = True