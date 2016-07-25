# -*- coding: utf-8 -*-
import codecs
import random
from trainTag import *
from testTag import *

trainFile = 'train.tag'
testFile = 'test.tag'

if __name__ == '__main__':
    trainSents = []
    testSents = []
    f = codecs.open(trainFile, 'r', encoding='utf-8')

    output = codecs.open('output_original.tag','w+','utf-8')
    # length = 0
    for line in f:
        # length += 1
        line = line.strip()
        if len(line) == 0:
            continue
        r = random.random()
        if r < 0.8:
            trainSents.append(line)
        else:
            testSents.append(line)
            output.write(line)
            output.write('\r\n')
    f.close()

    output.close()

    tr = trainTag(trainSents)
    tr.train()
    ts = testTag(testSents, tr.wordPosFreq, tr.posFreq, tr.posTransPro, tr.wordPosHeadPro, 'output.tag')
    ts.test()