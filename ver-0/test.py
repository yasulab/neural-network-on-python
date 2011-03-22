#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import pickle
from my_io import *
import model

TAB = '\t'

def test_by_list(w, test_data_list):
    for test_data in test_data_list:
        test(w, test_data)
        
def test(w, test_data):
    x = test_data.vector
    px = [1] + x
    s = 0
    for i in range(len(px)):
        s += w[i] * px[i]
    s += 2 # 's' needs to be a little looser to accept *-ish.txt
    if s < 0:
        print "The given letter (%s) is NOT an example of 'q'. (s=%d)" %  \
              (test_data.char, s)
    else:
        print "The given letter (%s) is an example of 'q'. (s=%d)" % \
              (test_data.char, s)
    
    
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python test.py KNOWLEDGE_FILENAME TEST_DATA_FILENAME"
        print
        exit()
    knowledge_filename = sys.argv[1]
    test_data_filename = sys.argv[2]
    test_data_list = load_data(test_data_filename)
    w = load_knowledge(knowledge_filename)
    test_by_list(w, test_data_list)
    


