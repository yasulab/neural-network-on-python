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
    def size_of_vector(self):
        return len(self.vector)
    
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

def save_data(filename, width, height, str):
    output = open(filename, "w")
    output.write(str)
    return


