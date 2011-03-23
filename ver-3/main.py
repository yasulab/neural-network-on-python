#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import pickle

class Data:
    def __init__(self, width, height, char, vector):
        self.width = width
        self.height = height
        self.char = char
        self.vector = vector

def load_data(filename):
    input = open(filename, "r")
    data_list = []
    info = input.readline()
    vector = []
    while info != "":
        width,height,char = info.split(" ")
        line = input.readline()
        while line != '\n' and line != "":
            for ch in line:
                if ch == '.':
                    vector.append(0)
                elif ch == 'X':
                    vector.append(1)
                else:
                    continue
            line = input.readline()
        data = Data(int(width), int(height), char.strip(), vector)
        data_list.append(data)
        vector = []
        info = input.readline()
    return data_list

# Nearest Neighbor Rule
def learn_nn(train_data_list, test_data_list, filename):
    for i,test in enumerate(test_data_list):
        d_list = []
        for train in train_data_list:
            d = 0
            for i in range(train.width*train.height):
                d += abs(train.vector[i] - test.vector[i])
            #print "d = %d" % d
            d_list.append(d)
        index = d_list.index(min(d_list))
        print "The given letter ('%s') is an example of '%s'. [Answer='%s']" % \
              (filename, train_data_list[index].char, test.char),
    return

def print_data(data):
    width = data.width
    height = data.height
    vector = data.vector
    i = 0
    for h in range(height):
        for w in range(width):
            if vector[i] == 0:
                print ".",
            elif vector[i] == 1:
                print "X",
            else:
                print "Print Data Eror"
            i += 1
        print
            
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python main.py TRAIN_FILENAME TEST_FILENAME"
        exit()
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    train_data_list = load_data(train_filename)
    test_data_list = load_data(test_filename)
    learn_nn(train_data_list, test_data_list, test_filename)
    

