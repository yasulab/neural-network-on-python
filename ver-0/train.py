#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import pickle
from my_io import *
import model

TAB = '\t'
BASE_LETTER = 'q' # Which letter you want to be correct?
TRAIN_TIMES = 100 # How many time you want to train?

# Pattern Recognition of Perceptron for AND
def and_by_perceptron(train_data):
    degree = len(train_data[0][0]) + 1 # 3: OK
    w = []
    for l in range(degree):
        w.append(0)
    #w = [0,0,0]
    
    for c in range(20): # c: How many inputs to learn
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

# Pattern Recognition of Nearest Neighbor Rule
def pr_nn(train_data_list, test_data_list):
    for i,test in enumerate(test_data_list):
        d_list = []
        for train in train_data_list:
            d = 0
            for j in range(train.width*train.height):
                d += abs(train.vector[j] - test.vector[j])
            #print "d = %d" % d
            d_list.append(d)
        index = d_list.index(min(d_list))
        print "Test data[%d] is an example of %s. [Answer='%s']" % \
              (i, train_data_list[index].char, test.char)
        print
    return

def get_weight(train_data_list):
    size_of_vector = train_data_list[0].size_of_vector() + 1
    w = []
    for l in range(size_of_vector):
        w.append(0)     # Create initial weight.

    print "CNVRG\ts(w*x)\tANSWER\tCORRECT?"
    for c in range(TRAIN_TIMES): # c: How many inputs to learn
        # shuffle 
        random.shuffle(train_data_list)
        
        # training
        n_errors = 0
        for train_data in train_data_list:
            # x: Given Input [x, y]
            x = train_data.vector
            # t: Correct Output (+1 or -1)
            if train_data.char == BASE_LETTER:
                #print "hoge!"
                t = +1
            else:
                t = -1
            
            px = [1] + x # px = phai(x) = [1, x, y]
            s = 0        # sigma w^T phai(x_n)
            for i in range(len(px)):
                s += w[i] * px[i] # sigma(w_i*x_i)
            if s * t <= 0: # If less than 0, it's error
                print str(c+1) + TAB ,     # Round
                #print w,       # Weight
                #print x,       # Randomly picked input
                print str(s) + TAB,       # Answer of Sigma
                print train_data.char + TAB, # Answer of char
                print t        # Is It Correct Output? (+1/-1)
                n_errors += 1
                for i in range(len(px)):
                    w[i] += t * px[i] # [w1,w2,w3]+=(+/-1)*[1,x,y]
                    
        if n_errors == 0:
            print "convergence: %d" %  c
            break
    #print "w = " +  str(w)
    return w

def test_by_perceptron(w, test_data):
    x = test_data.vector
    px = [1] + x
    s = 0
    for i in range(len(px)):
        s += w[i] * px[i]
    if s <= 0:
        print "The given letter (%s) is NOT an example of 'a'. (s=%d)" %  \
              (test_data.char, s)
    else:
        print "The given letter (%s) is an example of 'a'. (s=%d)" % \
              (test_data.char, s)
    
    
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python train.py TRAIN_DATA_FILENAME OUTPUT_FILENAME"
        print
        exit()
    train_filename = sys.argv[1]
    output_filename = sys.argv[2]
    train_data_list = load_data(train_filename)
    w = get_weight(train_data_list)
    save_knowledge(output_filename, w)
    print "Learned knowledge was written in '%s'.\n" % output_filename
    


