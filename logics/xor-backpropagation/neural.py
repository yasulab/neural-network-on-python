#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import math
import random
import sys

THRESHOLD = 0.05

class NeuralNet(object):
    """
    ﾊﾞｯｸﾌﾟﾛﾊﾟｹﾞｰｼｮﾝのﾊﾟｰｾﾌﾟﾄﾛﾝ
    """
    @property
    def inVals(self):
        return self._inVals

    @property
    def outVals(self):
        return self._outVals

    @property
    def inLayerNum(self):
        return self._inLayer

    @property
    def hiddenLayrNum(self):
        return self._hiddenLayer

    @property
    def outLaterNum(self):
        return self._outLayer
    
    def __init__(self, inLayer=0, hiddenLayer=0, outLayer=0, seed=0):
        if inLayer != 0 and hiddenLayer != 0 and outLayer != 0:
            self.createNetwork(inLayer, hiddenLayer, outLayer, seed)
            
    def createNetwork(self, inLayer, hiddenLayer, outLayer, seed=0):
        """
        初期ﾈｯﾄﾜｰｸを作る
        
        inLayer 入力層の数
        hiddenLayer 隠し層の数
        outLayer 出力層の数
        seed 初期ﾈｯﾄﾜｰｸの重みの乱数の種
        """
        random.seed(seed)

        self._inLayer = inLayer
        self._hiddenLayer = hiddenLayer
        self._outLayer = outLayer

        #入力層から隠れ層の重み
        self._w1 = [[random.uniform(-0.1, 0.1)
               for x in range(inLayer)]
              for y in range(hiddenLayer)]

        #隠れ層から出力層の重み
        self._w2 = [[random.uniform(-0.1, 0.1)
               for x in range(hiddenLayer)]
              for y in range(outLayer)]

        self._inVals = [0.0 for x in range(inLayer)]
        self._hiddenVals = [0.0 for x in range(hiddenLayer)]
        self._outVals = [0.0 for x in range(outLayer)]


    def compute(self, inVals):
        """
        NNに値を入力し結果を返す
        """
        sigmoid = lambda x: 1.0 / (1.0 + math.exp(-1 * x))

        self._inVals = inVals
                           
        #隠れ層の計算
        for i  in range(self._hiddenLayer):
            total = 0.0
            for j in range(self._inLayer):
                total += self._w1[i][j] * self._inVals[j]
            self._hiddenVals[i] = sigmoid(total)

        #出力層の計算
        for i in range(self._outLayer):
            total = 0.0
            for j in range(self._hiddenLayer):
                total += self._w2[i][j] * self._hiddenVals[j]
            self._outVals[i] = sigmoid(total)

        return self._outVals

    def backPropagation(self, teachVals, alpha=0.1):
        """
        ﾊﾞｯｸﾌﾟﾛﾊﾟｹﾞｰｼｮﾝによる学習
        """
        
        #隠れ層から出力層の重みの更新
        for i in range(self._outLayer):
            for j in range(self._hiddenLayer):
                delta = -alpha * ( -(teachVals[i] - self._outVals[i]) \
                                   * self._outVals[i] * (1.0 - self._outVals[i]) \
                                   * self._hiddenVals[j])
                self._w2[i][j] += delta

        #入力層から隠れ層の重みを計算する
        for i in range(self._hiddenLayer):
            total = 0.0
            for k in range(self._outLayer):
                total += self._w2[k][i] * (teachVals[k] - self._outVals[k]) \
                         * self._outVals[k] * (1.0 - self._outVals[k])
            for j in range(self._inLayer):
                delta = alpha * self._hiddenVals[i] * \
                        (1.0 - self._hiddenVals[i]) * self._inVals[j] * total
                self._w1[i][j] += delta

    def calcError(self, teachVals):
        """
        出力と教師信号との二乗誤差を求める｡
        """
        error = 0.0
        for i in range(self._outLayer):
            error += math.pow((teachVals[i] - self._outVals[i]), 2.0)
        error *= 0.5
        return error

def perceptron():
    input = [[1, 1], [1, 0], [0, 1], [0, 0]]
    output = [[0.0,], [1.0,], [1.0,], [0.0,]]

    nn = NeuralNet(2, 5, 1, 10)
    l = 0
    while 1:
        err = 0.0

        for (i, v) in zip(input, output):
            o = nn.compute(i)
            nn.backPropagation(v)
            err += nn.calcError(v)

        l += 1

        print l , ":Error->", err

        if(err < THRESHOLD):
            print "Error < " + str(THRESHOLD)
            break
        
    for i, v in zip(input, output):
        o = nn.compute(i)
        print "Input->", i,  "Output->", o, "Answer->", v
            
if __name__ == '__main__':
    argv_len = len(sys.argv)
    if argv_len != 2:
        print "Usage: python main.py TRAIN_DATA_FILENAME"
        exit()
    knowledge_filename = sys.argv[1]

    perceptron()