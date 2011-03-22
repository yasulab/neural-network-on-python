#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

INPUT = 2
HIDDEN = 2
OUTPUT = 1
PATTERN = 4
PR = 100
MAX_T = 10000
eta = 2.4
eps = 1.0e-4
alpha = 0.8
beta = 0.8
WO = 0.5

xi = v = o = zeta = []
w1 = w2 = [[]]
d_w1 = d_w2 = [[]]
pre_dw1 = pre_dw2 = [[]]
data = t_data = []

def load_data(filename):
    f = open(filename, "r")
    temp_list = []
    for p in range(PATTERN):
        temp_list.append( f.readline().split(" ") )
    for t in temp_list:
        data.append(([float(t[0]), float(t[1])], float(t[2].strip())))
    print data

def back_propagation():
    t,p,E,Esum = 0
    w_init()
    return

def w_init():
    return

if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 2:
        print "Usage: python train.py TRAIN_DATA_FILENAME OUTPUT_FILENAME"
        print        exit()
    train_filename = sys.argv[1]
    print eps
    load_data(train_filename)
    back_propagation()
    w_print()
