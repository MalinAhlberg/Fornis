# -*- coding: utf_8 -*-
import re
import itertools
import usefuls
import glob
from nltk.tokenize import PunktSentenceTokenizer
import cPickle as pickle
from xml.etree import ElementTree as etree
from padnums import pprint_table
import chunker

# dot or comma followed by a capital
#pOrC = list(itertools.chain(*[[',\s*'+c,'\.\s*'+c] for c in uppers]))


# ranks all files
def rankAll():
    ranks = []
    for fil in usefuls.allFiles:#['concattedParas/Alexius.xml']: #usefuls.concatFiles: #
       print "fil",fil
       #res = rankSpecial(pOrC,fil)
       #res = rankOne(fil,'.')
       res = rankText(fil)
       #res = countPara(fil)
       ranks += [res]
       if res is None:
          print "Noo",res
    printres(ranks,filepath='secbest') #,all=False,sorting=1)

minLength = 8
maxLength = 40

def rankSpecial(stops,fil):
    txt     = removePageN(extractText(fil))
    words   = groupwords(txt)
    whiteSpace = "\n\r\f\t\v"
    boundaries = whiteSpace+":;?!/"
    for s in boundaries:
       txt = map(lambda t: t.replace(s,' '),txt)
    stoptxt = putStops(stops,''.join(txt))
    ss      = stoptxt.split('!STOP!')
    lens    = []
    caps    = []
    for sent in ss:
      if bool(sent.strip()):
        lens += [len(sent.split())]
        caps += [sent.strip()[0].isupper()]
    mlen = mediumLen(lens)
    mediumCap1 = len(filter(lambda x: x, caps))/float(len(caps))
    res = {'rank' : 1,'Pleng' : mlen, 'caps' : mediumCap1, 'file' : fil}
    # returns rank 1, super good sentences
    print mlen
    if okLength(mlen):
        return res
    else: return {}

# put stops instead of stop, modify for use of real text, since
# in now removes all parts of 'stop'
def putStops(stops,txt):
    for s in stops:
       txt = re.sub(s,'!STOP!',txt)
    return txt


# extracts the relevant text from the xmls
def extractText(fil):
    inp  = open(fil,'r').read() 
    xml  = etree.fromstring(inp)
    txt  = ''
    #def addText(elem,txt):
    #    if not elem.text is None:
    #      txt += elem.text 
    body = xml.find(usefuls.prefix+'body')
    txt = ' '.join(body.itertext())
    return txt

def countPara(fil):
    inp   = open(fil,'r').read() 
    xml   = etree.fromstring(inp)
    body  = xml.find(usefuls.prefix+'body')
    sect  = body.find(usefuls.prefix+'section').findall(usefuls.prefix+'paragraph-definition')
    allPs = []
    for s in sect:
        allPs += s.iterfind('para')
    ss    = []
    for para in allPs:
        txt = list(para.itertext())
        if txt is not None and len(txt)>0:
          ss.append(' '.join(txt))
    ss = filter(lambda x : len(x.strip())>0,ss)
    (lens,_) =  countWords(ss)
    mlen = mediumLen(lens)
    res = {'rank' : 1,'Pleng' : mlen, 'caps' : 0, 'file' : fil}
    return res
 

# counts the length of the sentences and if they are followed
# by an upper case letter
def countSentence(txt,punkt): # , keep = False):
    if isinstance(punkt,list): # or keep:
       ss  = splitAny(txt,punkt)
    else:
       ss  = txt.split(punkt)
    return countWords(ss)

# counts the number of words in each element of 'ss'
def countWords(ss):
    whiteSpace = "\n\r\f\t\v"
    boundaries = whiteSpace+",.:;?!"
    for s in boundaries:
       ss = map(lambda t: t.replace(s,' '),ss)
    lens   = []
    uppers = []
    for sent in ss:
      sent = removePageN(sent)
      if bool(sent.strip()):
        lens   += [len(sent.split())]
        uppers += [sent.strip()[0].isupper()]
    return lens,uppers

# remove page numbering from text, so that it is not counted as a word
def removePageN(sent):
    sent  = re.sub(usefuls.re1,'',sent)
#    if not m is None:
#       sent = sent[:m.start()]+sent[m.start():]
    sent = re.sub(usefuls.re2,'',sent)
#    if not m2 is None:
#       sent = sent[:m.start()]+sent[m.start():]
    return sent

# classifies a file wrt the sentence length
def rankText(fil):
    txt = extractText(fil)
    # first count the sentences separated by '.'
    lens,caps = countSentence(txt,'.')
    mlen = mediumLen(lens)
    mediumCap1 = len(filter(lambda x: x, caps))/float(len(caps))
    res = {'rank' : 1,'Pleng' : mlen, 'caps' : mediumCap1, 'file' : fil}
    # returns rank 1, super good sentences
    if okLength(mlen):
        return res
    
    # then count the sentences separated by ','
    (klen,caps) = countSentence(txt,',')
    mklen = mediumLen(klen)
    mediumCap2 = len(filter(lambda x: x, caps))/float(len(caps))
    res.update({'rank' : 2,'Cleng' : mklen, 'caps' : mediumCap2})
    # returns rank 2, good sentences
    if okLength(mklen):
        return res

    # then count the sentences separated by capitalized words
    (xlen,_) = countSentence(txt,uppers)
    mxlen = mediumLen(xlen)
    res.update({'rank' : 3, 'Uleng' : mxlen, 'caps' : mediumCap1})
    # returns rank 3, ok sentenecs
    if okLength(mxlen):
       return res

    # then count the sentences separated by tabs
    (tlen,_) = countSentence(txt,'\t')
    mtlen = mediumLen(tlen)
    res.update({'rank': 4, 'tleng': mtlen})
    # returns rank 4, hard sentences
    return res

def mediumLen(xs):
    if len(xs)==0: 
      return 0
    else:
      return reduce(lambda x, y: x+y,xs)/float(len(xs))
def okLength(x):
    return x>=minLength and x<=maxLength

# count the sentences separated by 'stop'
def rankOne(fil,stop):
    txt = extractText(fil)
    lens,caps = countSentence(txt,stop) #,keep = True)
    mlen = mediumLen(lens)
    mediumCap1 = len(filter(lambda x: x, caps))/float(len(caps))
    res = {'rank' : 1,'Pleng' : mlen, 'caps' : mediumCap1, 'file' : fil}
    # returns rank 1, super good sentences
    if okLength(mlen):
        return res
    else: return {}
 
# classifies a file wrt the sentence length
def rankSuper():
    fils = glob.glob('sentenceSplit/*')
    lengs = ["File\tnltk sentence\tlength by '.'\t% capitalized after '.'\tlength by ','\t% capitalized after ','\t"
              +". or , and capital\tlength by capitals\tlength by tab\tparagraph length\ttotal length"""]
    model = getModel()
    for fil in fils:
      print 'file',fil
      inp   = open(fil,'r').read()
      xml   = etree.fromstring(inp)
      body  = xml.find(usefuls.prefix+'body')
      paras = body.findall('paragraph')
      ss = [] 
      len1,len2,cleng,caps,caps2,cpC,cap,tlen = [[] for x in range(8)]
      for para in paras:

          txt = list(para.itertext())
          if txt is not None and len(txt)>0:
            #txt = removePageN(' '.join(txt))
            txt = ' '.join(txt)
 
            # first count the sentences with nltk
            s    = model.tokenize(txt)
            (l,_) = countWords(s)
            len1 += (l)
    
            # then rank '.'
            l,c = countSentence(txt,'.')
            len2 += (l)
            caps += (c)
            
            # then count the sentences separated by ','
            (klen,capsC) = countSentence(txt,',')
            cleng += (klen)
            caps2 += (capsC)
    
            # then count the sentences separated by cpC
            s = chunker.grouptext(txt,'cpC')
            (l,_) = countWords(s)
            cpC += l
    
            # then count the sentences separated by capitalized words
            s = chunker.grouptext(txt,'cap')
            (l,_) = countWords(s)
            cap += (l)
    
            # then count the sentences separated by tabs
            (l,_) = countSentence(txt,'\t')
            tlen += (l)

            ss += [' '+txt]
 
      # calculate medium for the file
      normalleng = mediumLen(len1)
      dotleng = mediumLen(len2)
      caps = 0 if float(len(caps))==0 else len(filter(lambda x: x, caps))/float(len(caps))
      cleng = mediumLen(cleng)
      caps2 = 0 if float(len(caps2))==0 else len(filter(lambda x: x, caps2))/float(len(caps2))
      cpCleng = mediumLen(cpC)
      capleng = mediumLen(cap)
      tleng = mediumLen(tlen)

      txt = extractText(fil)
      (tot,_) = countWords([txt])
      totleng = mediumLen(tot)
      # then count the sentences separated by paras
     # inp   = open(fil,'r').read()
     # xml   = etree.fromstring(inp)
     # body  = xml.find(usefuls.prefix+'body')
     # paras = body.findall('paragraph')
     # for para in paras:
     #     txt = list(para.itertext())
     #     if txt is not None and len(txt)>0:
     #       ss.append(' '.join(txt))
      ss = filter(lambda x : len(x.strip())>0,ss)
      (lens,_) =  countWords(ss)
      paraleng = mediumLen(lens)

      row = [fil,normalleng,dotleng,caps,cleng,caps2,cpCleng,capleng,tleng,paraleng,totleng]
      lengs += ['\t'.join(map(lambda x: str(x),row))]

    table = '\n'.join(lengs)
    open('data3.txt','w').write(table)
    #pprint_table(open('data.txt','w'),lengs)

# read swedish model for segmenting
def getModel():
    model = "punkt-nltk-svenska.pickle"
    segmenter = PunktSentenceTokenizer
    with open(model, "rb") as M:
        model = pickle.load(M)
    segmenter_args = (model,)
    segmenter = segmenter(*segmenter_args)
    return segmenter


# upper case letters
uppers = list(u"ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖ")

# splits a text by some of a number of splitters
def splitAny(txt,stoppers):
    parts = []
    j = 0 
    for (i,c) in enumerate(txt):
        if c in stoppers:
           parts += [txt[j:i]]
           j = i
    parts += [txt[j:]]
    return parts
           
# formatting the output
def printres(res, filepath='best.txt',all=True,sorting=2):
   res.sort()
   s =  ""
   best = []
   good = []
   ok = []
   bad = []
   for b in res:
     fil   = b.get('file')
     pLeng = str(b.get('Pleng'))
     caps  = str(b.get('caps'))
     if b.get('rank')==1:
            best.append([fil,pLeng,caps])
     elif b.get('rank')==2:
        good.append([fil,str(b.get('Cleng')),caps,pLeng])
     else:
        s = [fil,str(b.get('Uleng')),caps,pLeng,str(b.get('Cleng'))]
        if b.get('rank')==3:
            ok.append(s)
        else:
          s = s+[str(b.get('tleng'))]
          bad.append(s)

     # sort 'best' by number of capitals after '.'
     best = sorted(best, key=lambda x: float(x[sorting]),reverse=True) 
     if all:
       # sort the others by sentence length
       good = sorted(good, key=lambda x: float(x[1]),reverse=True) 
       ok   = sorted(ok  , key=lambda x: float(x[1]),reverse=True) 
       bad  = sorted(bad , key=lambda x: float(x[1]),reverse=True) 

       goods = [["File","Sentence length for ','","Capital after ','"
                ,"Sentence length for '.'"]]+good
       oks   = [["File","Sentence length for capitals","Capital after '.'"
                ,"Sentence length for '.'","Sentence length for ','"]]+ok
       bads  = [["File","Sentence length for capitals","Capital after '.'"
                ,"Sentence length for '.'","Sentence length for ','","Sentence length for tab"]]+bad
       pprint_table(open('good.txt' ,'w'),goods)
       pprint_table(open('ok.txt'   ,'w'),oks)
       pprint_table(open('bad.txt' ,'w'),bads)

     bests = [["File","Sentence length for '.'","Capital after punctuation"]]+best
     pprint_table(open(filepath ,'w'),bests)

testfiles = ['../filerX/Birg-8.xml','../filerX/Bo.xml','../filerX/OgL-C.xml']


# the newest ranker
def rankNew():
    fils = glob.glob('sentenceSplit/*') # why sentenceSplit?
    lengs = ["File\tnltk sentence\tlength by '.'\t% capitalized after '.'\tlength by ','\t% capitalized after ','\t"
              +". or , and capital\tlength by capitals\tlength by tab\ttotal length"""]
    model = getModel()
    for fil in fils:
      print 'file',fil
      #txt = removePageN(extractText(fil))
      txt = (extractText(fil))

      # first count the sentences with nltk
      nltk    = model.tokenize(txt)
    
      # then rank '.'
      len2,caps = countSentence(txt,'.')
      
      # then count the sentences separated by ','
      (klen,caps2) = countSentence(txt,',')
    
      # then count the sentences separated by cpC
      ss = chunker.grouptext(txt,'cpC')
      (cpC,_) = countWords(ss)
    
      # then count the sentences separated by capitalized words
      ss = chunker.grouptext(txt,'cap')
      (cap,_) = countWords(ss)
    
      # then count the sentences separated by tabs
      (tlen,_) = countSentence(txt,'\t')

 
      (tot,_) = countWords([txt])
      print tot
      totlen = tot[0]
      # calculate medium for the file
      normalleng = div(totlen,nltk)
      dotleng = div(totlen,len2)
      caps = 0 if float(len(caps))==0 else len(filter(lambda x: x, caps))/float(len(caps))
      cleng = div(totlen,klen)
      caps2 = 0 if float(len(caps2))==0 else len(filter(lambda x: x, caps2))/float(len(caps2))
      cpCleng = div(totlen,cpC)
      capleng = div(totlen,cap)
      tleng   = div(totlen,tlen)

      # then count the sentences separated by paras
      inp   = open(fil,'r').read()
      xml   = etree.fromstring(inp)
      body  = xml.find(usefuls.prefix+'body')
      paras = body.findall('paragraph')

      row = [fil,normalleng,dotleng,caps,cleng,caps2,cpCleng,capleng,tleng,totlen]
      lengs += ['\t'.join(map(lambda x: str(x),row))]

    table = '\n'.join(lengs)
    open('data3.txt','w').write(table)
    #pprint_table(open('data.txt','w'),lengs)

def div(a,b):
    lenb = float(len(b))
    return lena if lenb==0 else float(a)/lenb
