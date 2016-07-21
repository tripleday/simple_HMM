# -*- coding: utf-8 -*-
import codecs
import random
from trainTag import *
from testTag import *

trainFile = 'conll2000train.txt'
testFile = 'conll2000test.txt'

if __name__ == '__main__':
    trainSents = []
    testSents = []
    f = codecs.open(trainFile, 'r', encoding='utf_8')
    # length = 0
    pairList = []
    for line in f:
        # length += 1
        line = line.strip()
        l = line.split(' ')
        # l.pop(1)
        pairList.append('/'.join(l[:2]))
        if len(line) == 0:
            r = random.random()
            if r < 0.7:
                trainSents.append(pairList)
            else:
                testSents.append(pairList)
            print pairList
            pairList = []
    f.close()

    # tr = trainTag(trainSents)
    # tr.train()
    # ts = testTag(testSents, tr.wordPosFreq, tr.posFreq, tr.posTransPro, tr.wordPosHeadPro, 'output.txt')
    # ts.test()