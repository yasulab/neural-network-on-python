#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import pickle

LAST_DATA = "last.dat"

class Data:
    def __init__(self, width, height, char, text):
        self.width = width
        self.height = height
        self.char = char
        self.text = text

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
    lines = []
    while info != "":
        width,height,c = info.split(" ")
        line = input.readline()
        while line != '\n' or "":
            lines.append(line)
            line = input.readline()
        data = Data(width, height, c, lines)
        data_list.append(data)
        lines = []
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
                print s,   # Sigma(w_i*x_i)
                print t    # Correct Output
                n_errors += 1
                for i in range(len(px)):
                    w[i] += t * px[i] # [w1,w2,w3]+=(+/-1)*[1,x,y]
                    
        if n_errors == 0:
            print "convergence: %d" %  c
            break
    return w

def learn_nn(train_data):
    return

if __name__ == '__main__':

    train_data = [ 
        [[0, 0], -1],
        [[1, 0], -1],
        [[0, 1], -1],
        [[1, 1], +1]
        ]

    print "Round w_i x_i sigma(w_i*x_i) Correct_Answer"
    w = learn_basic(train_data)
    print "w = " +  str(w)

    """
    w_last = load_knowledge(LAST_DATA)
    print "last w = " + str(w_last)
    save_knowledge(LAST_DATA, w)
    """

    """
    data_list = load_data("a.txt")
    #data_list = load_data("more-letters.txt")
    print
    for data in data_list:
        for line in data.text:
            print line
        print
    """ 


