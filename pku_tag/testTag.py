# -*- coding: utf-8 -*-
import math
import codecs

class wordNode:
    def __init__(self,word,posNodeList):
        self.word = word
        self.posNodeList = posNodeList

class posNode:
    def __init__(self,pos,cost,bestPath):
        self.pos = pos
        self.cost = cost
        self.bestPath = bestPath

class testTag:
    testSents = []          # sentences array
    wordPosFreq = {}        # wordPosFreq[word] = {pos1:fre1,pos2:fre2}. word and its pos:frequency
    posFreq = {}            # posFreq[pos] = fre. pos and its frequency
    posTransPro = {}        # posTransPro[pos] = {pos1:pro1,pos2:pro2}. probability of pos transferring to pos_x
    wordPosHeadPro = {}     # wordPosHeadPro[word] = {pos1:pro1,pos2:pro2}. word and its probability of being the head of sentence as pos
    outputFile = ''         # output file

    sentsNum = 0            # sentences num
    wordNum = 0             # words num
    correctNum= 0           # correct num
    correctRatio = 0        # correct ratio

    def __init__(self, sents, wordPosFreq, posFreq, posTransPro, wordPosHeadPro, outputFile):
        self.testSents = sents
        self.sentsNum = len(sents)
        self.wordPosFreq = wordPosFreq
        self.posFreq = posFreq
        self.posTransPro = posTransPro
        self.wordPosHeadPro = wordPosHeadPro
        self.outputFile = outputFile

    def test(self):
        output = codecs.open(self.outputFile,'w+','utf-8')
        print 'test:'
        for sent in self.testSents:
            wordList=[]# a list of wNode in one sentence
            index = -1

            pairList = sent.split('  ')# list of word/pos
            for pair in pairList:
                self.wordNum += 1
                index += 1

                word = pair.split('/')[0]# word

                if index == 0:
                    # 首节点
                    wNode = wordNode(word,[])
                    if self.wordPosFreq.has_key(word):
                        # 该词在词典中
                        if self.wordPosHeadPro.has_key(word):
                            # 当过句首
                            posHeadDic = self.wordPosHeadPro[word]# 获得该节点各词性当句首的概率
                            posHeadList = posHeadDic.keys()
                            for p in posHeadList:
                                cost = (-math.log(self.wordPosHeadPro[word][p]))
                                pNode=posNode(p,cost,[p])
                                wNode.posNodeList.append(pNode)

                            posList = self.wordPosFreq[word].keys()# 该节点所有词性
                            for p in posList:
                                if p not in posHeadList:# 该节点没当过句首的词性
                                    pNode=posNode(p,30,[p])
                                    wNode.posNodeList.append(pNode)
                        else:
                            # 没有当过句首
                            posFreqDic = self.wordPosFreq[word]
                            posList = posFreqDic.keys()# 获得该节点所有词性
                            for p in posList:
                                pNode=posNode(p,30,[p])
                                wNode.posNodeList.append(pNode)
                    else:
                        # 首节点不在词典中
                        # pNode=posNode('unknown',30,['unknown'])
                        # wNode.posNodeList.append(pNode)
                        posList = self.posFreq.keys()# 全局所有词性
                        for p in posList:
                            pNode=posNode(p,30,[p])
                            wNode.posNodeList.append(pNode)

                    wordList.append(wNode)
                else:
                    # 非首节点
                    wNode = wordNode(word,[])
                    if self.wordPosFreq.has_key(word):
                        # 该词在词典中
                        # 获取前一个节点的信息
                        preWNode = wordList[index-1]
                        prePosNodeList = preWNode.posNodeList

                        posFreqDic = self.wordPosFreq[word]
                        posList = posFreqDic.keys()# 获得该节点所有词性
                        # 对于每一种词性，计算最优路径
                        for p in posList:
                            minCost = 100000000
                            maxPreNode = posNode('',0,[])

                            # 对前一个节点每个词性，计算viterbi变量
                            for pn in prePosNodeList:
                                prePos = pn.pos# 前一个节点的某词性
                                preCost = pn.cost# 前一个节点取该词性的费用

                                # 转移概率
                                transProb = math.exp(-30)
                                if self.posTransPro.has_key(prePos):
                                    if self.posTransPro[prePos].has_key(p):
                                        transProb = self.posTransPro[prePos][p]

                                cost = preCost + (-math.log(transProb)) + (-math.log( 1.0*self.wordPosFreq[word][p]/self.posFreq[p] ))# 加上发射概率的代价
                                # 记录概率最大的词性以及路径（即费用最小）
                                if cost < minCost:
                                    minCost = cost
                                    maxPreNode = pn

                            # 记录通向word词性p的最佳路径
                            # path = maxPreNode.bestPath
                            path=[]
                            for e in maxPreNode.bestPath:
                                path.append(e)
                            path.append(p)
                            pNode = posNode(p,minCost,path)
                            wNode.posNodeList.append(pNode)
                    else: # 该词不在词典中，则将转移概率设为1
                        # 获取前一个节点的信息
                        preWNode = wordList[index-1]
                        prePosNodeList = preWNode.posNodeList

                        '''
                        minCost = 100000000
                        maxPreNode = posNode('',0,[])

                        # 对前一个节点每个词性，计算viterbi变量
                        for pn in prePosNodeList:
                            preCost = pn.cost
                            # 记录概率最大的词性以及路径
                            if preCost < minCost:
                                minCost = preCost
                                maxPreNode = pn

                        # 记录通向word的最佳路径
                        # path = maxPreNode.bestPath
                        path=[]
                        for e in maxPreNode.bestPath:
                            path.append(e)
                        path.append('unknown')
                        minCost += 0# 转移概率为1，代价0，发射概率的代价忽略为0
                        pNode = posNode('unknown',minCost,path)
                        wNode.posNodeList.append(pNode)
                        '''

                        posList = self.posFreq.keys()# 全局所有词性
                        # 对于每一种词性，计算最优路径
                        for p in posList:
                            minCost = 100000000
                            maxPreNode = posNode('',0,[])

                            # 对前一个节点每个词性，计算viterbi变量
                            for pn in prePosNodeList:
                                prePos = pn.pos# 前一个节点的某词性
                                preCost = pn.cost# 前一个节点取该词性的费用

                                # 转移概率
                                transProb = math.exp(-30)
                                if self.posTransPro.has_key(prePos):
                                    if self.posTransPro[prePos].has_key(p):
                                        transProb = self.posTransPro[prePos][p]

                                cost = preCost + (-math.log(transProb))
                                # 记录概率最大的词性以及路径（即费用最小）
                                if cost < minCost:
                                    minCost = cost
                                    maxPreNode = pn

                            # 记录通向word词性p的最佳路径
                            # path = maxPreNode.bestPath
                            path=[]
                            for e in maxPreNode.bestPath:
                                path.append(e)
                            path.append(p)
                            pNode = posNode(p,minCost,path)
                            wNode.posNodeList.append(pNode)

                    wordList.append(wNode)


            # 到达最后一个词
            lastWord = wordList[index]
            minCost = 100000000
            bestPath = []
            for pn in lastWord.posNodeList:
                if pn.cost < minCost:
                    minCost = pn.cost
                    bestPath = pn.bestPath


            index = -1
            pairList = sent.split('  ')# list of word/pos
            for pair in pairList:
                index += 1
                word = pair.split('/')[0]# word
                pos = pair.split('/')[1]# pos

                output.write(word)
                output.write('/' + bestPath[index] + '  ')
                if pos == bestPath[index]:
                    self.correctNum += 1
            output.write('\r\n')

        output.close()
        self.correctRatio = 1.0 * self.correctNum / self.wordNum

        print 'correctNum'
        print self.correctNum
        print 'wordNum'
        print self.wordNum
        print 'correctRatio'
        print self.correctRatio