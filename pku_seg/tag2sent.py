# -*- coding: utf-8 -*-
import codecs

inputFile = 'output.tag'
outputFile = 'output.seg'

if __name__ == '__main__':
    inputData = codecs.open(inputFile, 'r', 'utf-8')
    outputData = codecs.open(outputFile, 'w', 'utf-8')
    # 4 tags for character tagging: B(Begin), E(End), M(Middle), S(Single)
    for line in inputData.readlines():
        pariList = line.strip().split('  ')
        for pair in pariList:
            char = pair.split('/')[0]
            tag = pair.split('/')[1]
            if tag == 'B':
                outputData.write(char)
            elif tag == 'M':
                outputData.write(char)
            elif tag == 'E':
                outputData.write(char + '  ')
            else: # tag == 'S'
                outputData.write(char + '  ')
        outputData.write("\n")
    inputData.close()
    outputData.close()