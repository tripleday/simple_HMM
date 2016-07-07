# -*- coding: utf-8 -*-
import codecs
import random
from trainTag import *
from testTag import *

trainFile = 'train_utf16.tag'
testFile = 'test_utf16.tag'

if __name__ == '__main__':
    trainSents = []
    testSents = []
    f = codecs.open(trainFile, 'r', encoding='utf_16_le')
    # length = 0
    for line in f:
        # length += 1
        line = line.strip()
        if len(line) == 0:
            continue
        r = random.random()
        if r < 0.7:
            trainSents.append(line)
        else:
            testSents.append(line)
    f.close()

    tr = trainTag(trainSents)
    tr.train()
    ts = testTag(testSents, tr.wordPosFreq, tr.posFreq, tr.posTransPro, tr.wordPosHeadPro, 'output.tag')
    ts.test()