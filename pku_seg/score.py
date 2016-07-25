# -*- coding: utf-8 -*-
import codecs

originalFile = 'output_original.seg'
resultFile = 'output.seg'

correctTotal = 0
recallTotal = 0
precisionTotal = 0

if __name__ == '__main__':
    oData = codecs.open(originalFile, 'r', 'utf-8')
    # 4 tags for character tagging: B(Begin), E(End), M(Middle), S(Single)
    oIndexes = []
    for line in oData.readlines():
        phraseList = line.strip().split('  ')

        indexList = []
        base = 0
        for phrase in phraseList[:-1]:
            base += len(phrase)
            indexList.append(base)
        oIndexes.append(indexList)
    oData.close()


    rData = codecs.open(resultFile, 'r', 'utf-8')
    rIndexes = []
    for line in rData.readlines():
        phraseList = line.strip().split('  ')

        indexList = []
        base = 0
        for phrase in phraseList[:-1]:
            base += len(phrase)
            indexList.append(base)
        rIndexes.append(indexList)
    rData.close()


    for i in xrange(len(oIndexes)):
        o = oIndexes[i]
        r = rIndexes[i]
        correctTotal += len( set(o) & set(r) )
        recallTotal += len(o)
        precisionTotal += len(r)

    recallRate = 1.0 * correctTotal / recallTotal
    precisionRate = 1.0 * correctTotal / precisionTotal
    F = 2 / (1/recallRate + 1/precisionRate)

    print 'correctTotal'
    print correctTotal
    print 'recallTotal'
    print recallTotal
    print 'precisionTotal'
    print precisionTotal
    print 'recall rate'
    print recallRate
    print 'precision rate'
    print precisionRate
    print 'F'
    print F

