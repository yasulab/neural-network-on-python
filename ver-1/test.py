#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import pickle
from my_io import *
import model

TAB = '\t'

def winner_take_all(data_list, test_data):
    score_list = []
    char_list = []
    for data in data_list: # data[0] : w, data[1] : char
        score_list.append(get_score(data[0], test_data))
        char_list.append(data[1])
    #print score_list
    #print char_list
    win_score = max(score_list)
    win_char = char_list[score_list.index(win_score)]
    return (win_score, win_char)
                
def get_score(w, test_data):
    x = test_data.vector
    px = [1] + x
    s = 0
    for i in range(len(px)):
        s += w[i] * px[i]
    return s
    
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python test.py KNOWLEDGE_FILENAME TEST_DATA_FILENAME"
        print
        exit()
    knowledge_filename = sys.argv[1]
    test_data_filename = sys.argv[2]
    test_data_list = load_data(test_data_filename)
    data_list = load_knowledge(knowledge_filename)
    win_score,win_char = winner_take_all(data_list, test_data_list[0])
    print "The given letter ('%s')is an example of '%s'. (Score=%d)" % \
          (test_data_filename, win_char, win_score)
    


