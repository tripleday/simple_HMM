# -*- coding: utf-8 -*-
import codecs

inputFile = 'test_utf16.seg'
outputFile = 'test.tag'

if __name__ == '__main__':
    inputData = codecs.open(inputFile, 'r', 'utf_16_le')
    outputData = codecs.open(outputFile, 'w', 'utf-8')
    for line in inputData.readlines():
        for word in line.strip():
            outputData.write(word + '  ')
        outputData.write("\n")
    inputData.close()
    outputData.close()