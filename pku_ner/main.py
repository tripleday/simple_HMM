# -*- coding: utf-8 -*-
import codecs
import random
from trainTag import *
from testTag import *

trainFile = 'train_utf16.ner'
testFile = 'test_utf16.ner'

if __name__ == '__main__':
    trainSents = []
    testSents = []
    f = codecs.open(trainFile, 'r', encoding='utf_16_le')
    # length = 0
    pairList = []
    for line in f:
        # length += 1
        line = line.strip()
        if len(line) != 0:
            l = line.split(' ')
            pairList.append( [l[0], l[1]] )
        else:
            r = random.random()
            if r < 0.7:
                trainSents.append(pairList)
            else:
                testSents.append(pairList)
            pairList = []
    f.close()

    # f = codecs.open(testFile, 'r', encoding='utf_16_le')
    # # length = 0
    # pairList = []
    # for line in f:
    #     # length += 1
    #     line = line.strip()
    #     if len(line) != 0:
    #         l = line.split(' ')
    #         pairList.append( [l[0], l[1]] )
    #     else:
    #         testSents.append(pairList)
    #         pairList = []
    # f.close()

    tr = trainTag(trainSents)
    tr.train()
    ts = testTag(testSents, tr.wordPosFreq, tr.posFreq, tr.posTransPro, tr.wordPosHeadPro, 'output.ner')
    ts.test()