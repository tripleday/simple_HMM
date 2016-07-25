# -*- coding: utf-8 -*-
import codecs

inputFile = 'train_utf16.seg'
outputFile = 'train.tag'

if __name__ == '__main__':
    inputData = codecs.open(inputFile, 'r', 'utf_16_le')
    outputData = codecs.open(outputFile, 'w', 'utf-8')
    for line in inputData.readlines():
        wordList = line.strip().split('  ')
        for word in wordList:
            if len(word) == 1:
                outputData.write(word + "/S  ")
            else:
                outputData.write(word[0] + "/B  ")
                for w in word[1:-1]:
                    outputData.write(w + "/M  ")
                outputData.write(word[-1] + "/E  ")
        outputData.write("\n")
    inputData.close()
    outputData.close()