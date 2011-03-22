#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
import random
import pickle
from my_io import *
import math

# As THRESHOLD goes down, it takes more time to learn,
# but you can get an answer more accurately.
THRESHOLD = 0.15

"""
TODO: change this into winnter-take-all one.
"""
BASE_LETTER = 'q'

# Back Propagation of Perceptron
class NeuralNet(object):
    def __init__(self, in_layer=0, hidden_layer=0, out_layer=0, seed=0):
        """
        Creating Initial Network        
        - in_layer: Num of in_layer
        - hidden_layer: Num of hidden_layer
        - out_layer: Num of out_layer
        - seed: seed for random
        """
        random.seed(seed)

        self._in_layer = in_layer
        self._hidden_layer = hidden_layer
        self._out_layer = out_layer

        # weight from in_layer to hidden_layer
        self._w1 = [[random.uniform(-0.1, 0.1)
                    for x in range(in_layer)]
                    for y in range(hidden_layer)]

        # weight from hidden_layer to out_layer
        self._w2 = [[random.uniform(-0.1, 0.1)
                    for x in range(hidden_layer)]
                    for y in range(out_layer)]

        self._in_vals = [0.0 for x in range(in_layer)]
        self._hidden_vals = [0.0 for x in range(hidden_layer)]
        self._out_vals = [0.0 for x in range(out_layer)]


    def compute(self, in_vals):
        """
        Store input valut at NeuralNet and return its result.
        """
        sigmoid = lambda x: 1.0 / (1.0 + math.exp(-1 * x))

        self._in_vals = in_vals
                           
        # calculation in hidden_layer
        for i  in range(self._hidden_layer):
            total = 0.0
            for j in range(self._in_layer):
                total += self._w1[i][j] * self._in_vals[j]
            self._hidden_vals[i] = sigmoid(total)

        # calculation in out_layer
        for i in range(self._out_layer):
            total = 0.0
            for j in range(self._hidden_layer):
                total += self._w2[i][j] * self._hidden_vals[j]
            self._out_vals[i] = sigmoid(total)

        return self._out_vals

    def back_propagation(self, teach_vals, alpha=0.1):
        """
        Learn by Back Propagation
        """
        
        # update weight from hidden_layer to out_layer
        for i in range(self._out_layer):
            for j in range(self._hidden_layer):
                delta = -alpha * ( -(teach_vals[i] - self._out_vals[i]) \
                                   * self._out_vals[i] * (1.0 - self._out_vals[i]) \
                                   * self._hidden_vals[j])
                self._w2[i][j] += delta

        # update weight from in_layer to hidden_layer
        for i in range(self._hidden_layer):
            total = 0.0
            for k in range(self._out_layer):
                total += self._w2[k][i] * (teach_vals[k] - self._out_vals[k]) \
                         * self._out_vals[k] * (1.0 - self._out_vals[k])
            for j in range(self._in_layer):
                delta = alpha * self._hidden_vals[i] * \
                        (1.0 - self._hidden_vals[i]) * self._in_vals[j] * total
                self._w1[i][j] += delta

    def calc_error(self, teach_vals):
        """
        (Difference between _out_vals and teach_vals)^2
        """
        error = 0.0
        for i in range(self._out_layer):
            error += math.pow((teach_vals[i] - self._out_vals[i]), 2.0)
        error *= 0.5
        return error

def perceptron(train_data_list):
    """
    # Sample input / output
    input = [
        [1, 1],
        [1, 0],
        [0, 1],
        [0, 0]
        ]
    output = [
        [0.0],
        [1.0],
        [1.0],
        [0.0]
        ]
    """
    n_in_layer = train_data_list[0].size_of_vector()
    # n_hidden_layer = 5 # This is optional
    n_out_layer = len(train_data_list)
    print n_in_layer, n_out_layer
    input = []
    output = []
    for train_data in train_data_list:
        input.append(train_data.vector)
        if train_data.char == BASE_LETTER:
            output.append([1.0])
        else:
            output.append([0.0])
    print output
    print input
    #exit()
    # NeuralNet(in_layer, hidden_layer, out_layer, seed)
    nn = NeuralNet(n_in_layer, 5, 1, 10)
    """
    Creating Initial Network        
    - in_layer: Num of in_layer
    - hidden_layer: Num of hidden_layer
    - out_layer: Num of out_layer
    - seed: seed for random
    """
    
    n_errors = 0
    while 1:
        err = 0.0
        
        for (i, v) in zip(input, output):
            o = nn.compute(i)       #
            nn.back_propagation(v)   #
            err += nn.calc_error(v)  #

        n_errors += 1

        print n_errors , ":Error->", err

        if(err < THRESHOLD):
            print "Error < " + str(THRESHOLD)
            break

    return nn

def test(nn, test_data_list):
    """
    Final Test - check if the result is correct.
    """
    input = []
    output = []
    for test_data in test_data_list:
        input.append(test_data.vector)
        if test_data.char == BASE_LETTER:
            output.append([1.0])
        else:
            output.append([0.0])

    i = 0
    for inp, v in zip(input, output):
        o = nn.compute(inp)
        #print "Input->", inp,
        print "The given letter ('%s') score is " %  test_data_list[i].char,
        print o,
        print "(Answer = ", v, ")"
        i += 1
        
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 3:
        print "Usage: python main.py TRAIN_DATA_FILENAME TEST_DATA_FILENAME"
        exit()
    train_data_filename = sys.argv[1]
    test_data_filename = sys.argv[2]
    train_data_list = load_data(train_data_filename)
    test_data_list = load_data(test_data_filename)

    nn = perceptron(train_data_list)
    
    """
    TODO: Unable to pickle my own class.
    """
    # save_knowledge(nn, output_filename)
    # print "Learned knowledge was written in '%s'.\n" % output_filename
    # print

    test(nn, test_data_list)
    







