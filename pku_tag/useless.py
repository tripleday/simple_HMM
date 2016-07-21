# -*- coding: cp936 -*-

###librarys:
import codecs
import sys


### global variables:
freqdic={}
dic={}
transferdic={}
inputfilename=''
outputfilename=''
trainingfilename=''
marklist=[]

###classes:
class nodeinfotable:
    def __init__(self,No,length,previousdict):
        self.No=No
        self.length=length
        self.previousdict=previousdict

class node:
    def __init__(self,outpointerdict,tablelist):
        self.outpointerdict=outpointerdict
        self.tablelist=tablelist
    def addOutPointer(self,targetnum,wordname):
        self.outpointerdict[targetnum]=wordname


class wordnode:
    def __init__(self,wordval,propertynodelist):
        self.wordval=wordval
        self.propertynodelist=propertynodelist

class propertynode:
    def __init__(self,propertyval,probability,beststack):
        self.propertyval=propertyval
        self.probability=probability
        self.beststack=beststack


###functions:
#find cmpstr in valuestr,which is splited by ','
def findinstr(valuestr,cmpstr):
    wordlist=valuestr.split(',')
    for w in wordlist:
        if cmpstr==w:
            return True
    return False

# generate the dictionary
def chnsegtager_training():
    global dic
    global freqdic
    global transferdic
    transfercounter=0
    wordcounter=0
    orgname = ''
    f = codecs.open(trainingfilename, 'r', encoding='utf_16_le')
    # ls = [ line.strip() for line in f ]
    for line in f:
        line=line.strip()
        if len(line)==0:
            continue
        linewordindex=0
        prewordproperty=''
        currwordproperty=''
        if line.find('/') != -1:
            lineset = line.split('  ')
            # print lineset
            for w in lineset:# 对于一行中每一个字母
                wordcounter+=1
                singlewordset = w.split('/')
                formerword = singlewordset[0]# 单词
                laterword = singlewordset[1]# 标注

                if dic.has_key(formerword):# 字典里存在此单词
                    if freqdic.has_key(formerword+','+laterword):
                        freqdic[formerword+','+laterword]+=1
                    else:
                        freqdic[formerword+','+laterword]=1
                    valueStr = dic[formerword]
                    if findinstr(valueStr,laterword)==False:
                        dic[formerword] += ','+laterword
                else:# 字典不存在，创建
                    dic[formerword] = laterword
                    freqdic[formerword+','+laterword]=1

                linewordindex+=1
                if linewordindex==1:
                    currwordproperty=laterword# 第一个单词
                else:
                    prewordproperty=currwordproperty
                    currwordproperty=laterword
                    transstr=prewordproperty+':'+currwordproperty
                    if transferdic.has_key(transstr):
                        transferdic[transstr]+=1
                        transfercounter+=1
                    else:
                        transferdic[transstr]=1
                        transfercounter+=1
    # 统计转移概率
    for trstr,trnum in transferdic.items():
        pcl=float(trnum)
        probability=pcl/transfercounter
        transferdic[trstr]=probability

    # 统计词频
    for fx,lx in freqdic.items():
        nlx=float(lx)
        prox=nlx/wordcounter
        freqdic[fx]=prox

    f.close()

#get the file name from command line
def getArguments():
    global inputfilename,outputfilename,trainingfilename
    #sys.argv += ['input.txt','output.txt']
    # if len(sys.argv) < 3:
    #     print 'Error:No file specified.(arg1:name of input file; arg2:name of output file; arg3:training file name'
    #     sys.exit()
    inputfilename = 'C:/Users/Wu/Desktop/nlp/Tag/test_utf16.tag'
    outputfilename = 'C:/Users/Wu/Desktop/nlp/Tag/output.tag'
    trainingfilename='C:/Users/Wu/Desktop/nlp/Tag/train_utf16.tag'

#get the punctuation marks in the dict
# def getMarksList():
#     global dic,freqdic,marklist
#     for f,l in dic.items():
#         if l=='w':
#             marklist.append(f)


#check if the character is a mark
# def checkMark(unicha):
#     for w in marklist:
#         uniw=w
#         if uniw==unicha:
#             return True
#     return False

#process single sentance
def processSentence(unisent,unisymbol):
    global inputfilename,outputfilename
    # if len(unisent)==0:
    #     gbksy = unisymbol.encode('utf_16_le')
    #     if gbksy!='' and gbksy!='\n':
    #         savefile=file(outputfilename,'a')
    #         savefile.write(gbksy+'//w'.encode('utf_16_le'))
    #         savefile.write('  '.encode('utf_16_le'))
    #         savefile.close()
    #     return
    global dic,freqdic
    nodelist=[] #store the word in the the single phrase
    index=0
    sentlen=len(unisent.split('  '))
    print unisent.split('  ')
    for w in unisent.split('  '):
        index+=1 #index is the character behind w
        #---------add the single word edge----------
        print '***************************************'
        gbksingleword=w.encode('utf_16_le')
        if dic.has_key(gbksingleword):
            newnode=node({gbksingleword:dic[gbksingleword]},[])
        else:
            newnode=node({gbksingleword:'unknown'},[])

        if index==sentlen:  #reach the last element
            nodelist.append(newnode)
            break
        #newnode= node({},[])#make a node
        unistrafterw=unisent[index:]
        fw=w
        lw=u''
        for bw in unistrafterw:
            lw+=bw
            uniword=fw+lw
            gbkword=uniword.encode('utf_16_le')
            if dic.has_key(gbkword):#create a chain
                newnode.outpointerdict[gbkword]=dic[gbkword]
        nodelist.append(newnode)

    print nodelist

    lastnode=node({},[])
    nodelist.append(lastnode)

    #generate the information table for each node
    nodeindex=0 #the index of the current node
    for nodeitem in nodelist:   #nodeitem:node
        if nodeindex==0:
            nodeindex+=1
            continue
        if nodeindex==1:
            newtableitem=nodeinfotable(1,1,{0:0})
            nodeitem.tablelist.append(newtableitem)
            nodeindex+=1
            continue
        No=0 #the sequence number of the table item for each node
        prelist = nodelist[:nodeindex] #nodes before the nodeitem
        preindex=0
        for prenode in prelist:#node in before nodeitem
            for wordname,wordproperty in prenode.outpointerdict.items():
                uniwordname=wordname
                wordlength=len(uniwordname)
                if nodeindex==(preindex+wordlength):#exist a pointer to current node
                    if preindex==0:
                        No+=1
                        newtableitem=nodeinfotable(No,1,{0:0})
                        nodeitem.tablelist.append(newtableitem)
                    else:
                        preNo=0 #sequence of tableitem number in the prenode
                        for pretableitem in prenode.tablelist:#pretableitem:nodeinfotable in the prenode
                            preNo+=1
                            No+=1
                            newtableitem=nodeinfotable(No,pretableitem.length+1,{preindex:preNo})#add the item
                            nodeitem.tablelist.append(newtableitem)
            preindex+=1
        nodeindex+=1

    n=0

    #find all the partition results in nodelist[], and store them into a hashtable
    pathhashtable={}
    tailnode=nodelist[-1]
    tailnodenum=len(nodelist)-1
    for tableitem in tailnode.tablelist:    #tableitem:single table item of the last node
        pathlength=tableitem.length #the length of the path
        for ff,fl in tableitem.previousdict.items():
            prenodenumber=ff
        pathstack=[tailnodenum]
        iteritem=tableitem
        while prenodenumber!=0: #go until reach the node 0
            for f,l in iteritem.previousdict.items():  #exactly, there is noly one item in the dict
                prenodenumber=f #previous node number
                prenodeitemnumber=l #the number of sequence item of the previous node
            pathstack.insert(0,prenodenumber)
            iteritem=nodelist[prenodenumber].tablelist[prenodeitemnumber-1]
            for f,l in iteritem.previousdict.items():  #update data
                prenodenumber=f #previous node number
                prenodeitemnumber=l #the number of sequence item of the previous node
        pathstack.insert(0,0)
        pathhashtable[pathlength]=pathstack

    print pathhashtable
    xulie=0
    shortestpath = []
    for length,path in pathhashtable.items():
        if xulie==0:
            minlen=length
            shortestpath=path
        else:
            if length<minlen:
                minlen=length
                shortestpath=path
        xulie+=1

    #generate the result of rough split of the single sentence
    uniresultlist=[]
    for n in shortestpath:
        if n==0:
            findex=n
            continue
        lindex=n
        oneword=unisent[findex:lindex]
        findex=lindex
        uniresultlist.append(oneword)
    print uniresultlist

    #check if it is numbers or combination of numbers, or dates,times,plus,
    # unidatetime=[u'年',u'月',u'日',u'时',u'分',u'秒']
    # uniquantifier=[u'亿',u'万',u'千',u'百',u'十',u'个']
    # unioperator=[',','.','+','-','*','%','@',u'％']
    # unidicquantifier=[]
    # for f,l in dic.items():
    #     if l.find('q')!=-1:
    #         uniqua=f
    #         if len(uniqua)==1:
    #             unidicquantifier.append(uniqua)
    # unisymbollist=unidatetime+uniquantifier+unioperator+unidicquantifier

    # qword=''
    # resultindex=0
    # uninewlist=[]
    # for uniword in uniresultlist:
    #     if len(uniword)==1:
    #         gbkupperword=uniword.encode('utf_16_le')
    #         if (isDigit(uniword))or(uniword in unisymbollist)or(gbkupperword.isalpha()):
    #             qword+=uniword
    #         else:
    #             uninewlist.append(qword)
    #             uninewlist.append(uniword)
    #             gbkw=qword.encode('utf_16_le')
    #             if len(gbkw)!=0:
    #                 dic[gbkw]='m'
    #                 if freqdic.has_key(gbkw+',m'):
    #                     freqdic[gbkw+',m']+=1
    #                 else:
    #                     freqdic[gbkw+',m']=1
    #             qword=''
    #     else:
    #         if qword!='':
    #             gbkw=qword.encode('utf_16_le')
    #             if len(gbkw)!=0:
    #                 dic[gbkw]='m'
    #                 if freqdic.has_key(gbkw+',m'):
    #                     freqdic[gbkw+',m']+=1
    #                 else:
    #                     freqdic[gbkw+',m']=1
    #             uninewlist.append(qword)
    #             qword=''
    #         uninewlist.append(uniword)
    #     resultindex+=1
    # if len(qword)!=0:
    #     uninewlist.append(qword)
    #
    unilastlist=[]
    for w in uniresultlist:
        if len(w)!=0:
            unilastlist.append(w)

    #使用viterbi算法进行词性标注
    vtbwordlist=[]
    index=-1
    hmmwordlist=[]
    print unilastlist
    for uniword in unilastlist:
        index+=1
        word=uniword.encode('utf_16_le')
        if index==0:
            #创建首节点
            if dic.has_key(word):
                firstpstr=dic[word]
                firstproplist=firstpstr.split(',')
                wnode=wordnode(word,[])
                for p in firstproplist:
                    #计算符号到当前词的转移概率
                    # if transferdic.has_key('w,'+p):
                    #     pronode=propertynode(p,transferdic['w,'+p],[p])
                    # else:
                    pronode=propertynode(p,1e-10,[p])
                    wnode.propertynodelist.append(pronode)
                hmmwordlist.append(wnode)
            else:
                #首节点未在字典定义
                pronode=propertynode('m',1e-10,['m'])
                wnode=wordnode(word,[pronode])
                hmmwordlist.append(wnode)
        else: #Index不为0
            nowwordnode=wordnode(word,[])
            #先取得当前结点的属性
            if dic.has_key(word):
                prostr=dic[word]
                prostrlist=prostr.split(',')#当前节点的词性集
                for p in prostrlist:
                    #对于每一种属性，由前节点进行最优路径计算
                    #取得前结点属性
                    prewordnode=hmmwordlist[index-1]
                    prepronodelist=prewordnode.propertynodelist
                    maxprobability=0
                    maxprenode=propertynode('',1,[])
                    for pnode in prepronodelist:
                        #对于前节点的每个词性，进行viterbi计算
                        prepbt=pnode.probability
                        preprop=pnode.propertyval
                        transtr=preprop+':'+p
                        if transferdic.has_key(transtr):
                            transprobability=transferdic[transtr]
                        else:
                            transprobability=1e-10#不存在此转移，赋一个极小的值
                        nowprobability=prepbt*transprobability
                        if nowprobability>maxprobability:
                            maxprobability=nowprobability
                            #maxprenode=pnode
                            maxprenode.propertyval=pnode.propertyval
                            maxprenode.probability=pnode.probability
                            maxprenode.beststack=pnode.beststack
                    nowbeststack=[]
                    for se in maxprenode.beststack:
                        nowbeststack.append(se)
                    nowbeststack.append(p)
                    pronode=propertynode(p,maxprobability,nowbeststack)
                    nowwordnode.propertynodelist.append(pronode)
            else:
                #字典不存在此词，则将转移概率置为1
                #取得前结点的所有词性集，然后取最大概率词性，生成当前结点的最优路径
                prewordnode=hmmwordlist[index-1]
                prepronodelist=prewordnode.propertynodelist
                maxprobability=0
                for pnode in prepronodelist:
                    prepbt=pnode.probability
                    if prepbt>maxprobability:
                        maxprobability=prepbt
                        maxprenode=pnode

                nowbeststack=[]
                for se in maxprenode.beststack:
                    nowbeststack.append(se)
                nowbeststack.append('nz')
                pronode=propertynode('nz',maxprobability,nowbeststack)
                nowwordnode.propertynodelist.append(pronode)
            hmmwordlist.append(nowwordnode)

    print index
    print hmmwordlist
    hmmlastword=hmmwordlist[index]
    maxp=0
    for l in hmmlastword.propertynodelist:
        if maxp<l.probability:
            maxp=l.probability
            maxn=l

    stackindex=0
    savefile=file(outputfilename,'a')
    for w in unilastlist:
        print '**********************************************'
        uniw=w.encode('utf_16_le')
        if uniw!='' and uniw!='\n':
            savefile.write(uniw)
            savefile.write(('/'+l.beststack[stackindex]).encode('utf_16_le'))
            stackindex+=1
            savefile.write('  '.encode('utf_16_le'))


    # gbksymb=unisymbol.encode('utf_16_le')#写标点符号
    # if gbksymb!='' and gbksymb!='/n':
    #     savefile.write(gbksymb)
    #     savefile.write('//w')
    #     savefile.write('  ')
    savefile.close()



#check if unistr is a digit
def isDigit(unistr):
    if unistr.isdigit():
        return True
    unichadigit=u'一二三四五六七八九十'
    if unistr in unichadigit:
        return True
    return False


#partition
def chnsegtager_segtag():
    global inputfilename,outputfilename
    global dic,freqdic
    infile=file(inputfilename)
    # getMarksList()
    f = codecs.open(inputfilename, 'r', encoding='utf_16_le')
    for line in f:
        line=line.strip()
        if len(line)==0:
            continue
        uniline=line
        bufstr=u''

        print uniline.split('  ')
        # for w in uniline:
        processSentence(uniline, bufstr) #process bufstr as a block
        bufstr=u''
        # if len(w)!=0:
        #     processSentence(bufstr,'/n')
        #     bufstr=u''

        savefile=file(outputfilename,'a')
        savefile.write('\n')
        savefile.close()

    infile.close()

def clearFile():
    f = file(outputfilename,'w')
    f.write('')
    f.close()

###execution segments:
getArguments()
clearFile()
chnsegtager_training()
chnsegtager_segtag()
