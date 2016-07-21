# -*- coding: utf-8 -*-

class trainTag:
    trainSents = []         # sentences array
    sentsNum = 0            # sentences num
    wordNum = 0             # words num
    wordPosFreq = {}        # wordPosFreq[word] = {pos1:fre1,pos2:fre2}. word and its pos:frequency
    posFreq = {}            # posFreq[pos] = fre. pos and its frequency
    posTransFreq = {}       # posTransFreq[pos] = {pos1:frq1,pos2:frq2}. frequency of pos transferring to pos_x
    posTransPro = {}        # posTransPro[pos] = {pos1:pro1,pos2:pro2}. probability of pos transferring to pos_x
    wordPosHeadFreq = {}    # wordPosHeadFreq[word] = {pos1:fre1,pos2:fre2}. word and its frequency of being the head of sentence as pos
    wordPosHeadPro = {}     # wordPosHeadPro[word] = {pos1:pro1,pos2:pro2}. word and its probability of being the head of sentence as pos

    def __init__(self, sents):
        self.trainSents = sents
        self.sentsNum = len(sents)

    def train(self):
        print 'training:'
        for sent in self.trainSents:
            prePos = ''
            currPos = ''

            index = -1
            pairList = sent.split('  ')# list of word/pos
            for pair in pairList:
                self.wordNum += 1
                index += 1

                word = pair.split('/')[0]# word
                pos = pair.split('/')[1]# pos

                # 统计该词性的频数
                if self.posFreq.has_key(pos):
                    self.posFreq[pos] += 1
                else:
                    self.posFreq[pos] = 1

                # 统计该词以该词性出现的频数
                if self.wordPosFreq.has_key(word):
                    # 字典里存在该词
                    posList = self.wordPosFreq[word].keys()
                    if pos in posList:
                        self.wordPosFreq[word][pos] += 1
                    else:
                        self.wordPosFreq[word][pos] = 1
                else:
                    # 字典不存在该词则创建
                    self.wordPosFreq[word] = {}
                    self.wordPosFreq[word][pos] = 1

                # 统计词性转移的频数
                if index == 0:# 句首
                    currPos = pos  # 记录句首词的词性
                    # 统计该词以该词性出现在句首的频数
                    if self.wordPosHeadFreq.has_key(word):
                        # 字典里存在该词
                        posList = self.wordPosHeadFreq[word].keys()
                        if pos in posList:
                            self.wordPosHeadFreq[word][pos] += 1
                        else:
                            self.wordPosHeadFreq[word][pos] = 1
                    else:
                        # 字典不存在该词则创建
                        self.wordPosHeadFreq[word] = {}
                        self.wordPosHeadFreq[word][pos] = 1
                else:# 非句首
                    prePos = currPos
                    currPos = pos
                    if self.posTransFreq.has_key(prePos):  # 记录句中两种词性相邻的次数
                        toPosList = self.posTransFreq[prePos].keys()
                        if currPos in toPosList:
                            self.posTransFreq[prePos][currPos] += 1
                        else:
                            self.posTransFreq[prePos][currPos] = 1
                    else:
                        self.posTransFreq[prePos] = {}
                        self.posTransFreq[prePos][currPos] = 1

        # 计算转移概率
        for fromPos in self.posTransFreq.keys():
            posTransDic = self.posTransFreq[fromPos]
            posSum = sum(posTransDic.values())
            self.posTransPro[fromPos] = {}
            for toPos in posTransDic.keys():
                self.posTransPro[fromPos][toPos] = 1.0 * posTransDic[toPos] / posSum

        # 计算句首词性概率
        for word in self.wordPosHeadFreq.keys():
            posHeadDic = self.wordPosHeadFreq[word]
            posSum = sum(posHeadDic.values())
            self.wordPosHeadPro[word] = {}
            for pos in posHeadDic.keys():
                self.wordPosHeadPro[word][pos] = 1.0 * posHeadDic[pos] / posSum