#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import pickle

LAST_DATA = "last.dat"

class Data:
    def __init__(self, width, height, char, vector):
        self.width = width
        self.height = height
        self.char = char
        self.vector = vector

def save_knowledge(filename, data):
    f = open(filename, 'w')
    pickle.dump(data, f)
    f.close()
    
def load_knowledge(filename):
    f = open(filename)
    return pickle.load(f)

def load_data(filename):
    input = open(filename, "r")
    data_list = []
    info = input.readline()
    vector = []
    while info != "":
        width,height,char = info.split(" ")
        line = input.readline()
        while line != '\n' or "":
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

def save_data(filename, width, height, str):
    output = open(filename, "w")
    output.write(str)
    return

def learn_basic(train_data):
    degree = len(train_data[0][0]) + 1 # 3: OK
    w = []
    for l in range(degree):
        w.append(0)
    #w = [0,0,0]
    #w = load_knowledge(LAST_DATA)
    
    for c in range(20): # c: How many times to learn
        # shuffle 
        random.shuffle(train_data)
        
        # training
        n_errors = 0
        for x,t in train_data:
            # x: Given Input [x, y]
            # t: Correct Output (+1 or -1)
            px = [1] + x # px = phai(x) = [1, x, y]
            s = 0        # sigma w^T phai(x_n)
            for i in range(len(px)):
                s += w[i] * px[i] # [w1, w2, w3] * [1, x, y]
            if s * t <= 0: # If (sigma*output) is less than 0 -> error
                print c+1, # Round
                print w,   # Weight
                print px,  # Randomly picked input
                print s,   # Answer of Sigma
                print t    # Correct Output
                n_errors += 1
                for i in range(len(px)):
                    w[i] += t * px[i] # [w1,w2,w3]+=(+/-1)*[1,x,y]
                    
        if n_errors == 0:
            print "convergence: %d" %  c
            break
    return w

# Nearest Neighbor Rule
def learn_nn(train_data_list, test_data_list):
    for i,test in enumerate(test_data_list):
        d_list = []
        for train in train_data_list:
            d = 0
            for i in range(train.width*train.height):
                d += abs(train.vector[i] - test.vector[i])
            #print "d = %d" % d
            d_list.append(d)
        index = d_list.index(min(d_list))
        print "Test data[%d] is an example of %s. [Answer='%s']" % \
              (index, train_data_list[index].char, test.char),
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

    train_and_data = [ 
        [[0, 0], -1],
        [[1, 0], -1],
        [[0, 1], -1],
        [[1, 1], +1]
        ]
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python main.py TRAIN_FILENAME TEST_FILENAME"
        exit()
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    train_data_list = load_data(train_filename)
    test_data_list = load_data(test_filename)
    learn_nn(train_data_list, test_data_list)
    #print test_data_list[0].vector
    #print_data(test_data_list[0])
    #w = learn_basic(train_and_data)
    #print "w = " +  str(w)

    """
    w_last = load_knowledge(LAST_DATA)
    print "last w = " + str(w_last)
    save_knowledge(LAST_DATA, w)
    """

    """
    data_list = load_data("TestSet.txt")
    data_list = load_data("a.txt")
    #data_list = load_data("more-letters.txt")
    print
    for data in data_list:
        for line in data.text:
            print line
        print
    """ 

