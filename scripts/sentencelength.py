# -*- coding: utf_8 -*-
import re
import itertools
import usefuls
from xml.etree import ElementTree as etree
from padnums import pprint_table

# dot or comma followed by a capital
pOrC = list(itertools.chain(*[[',\s*'+c,'\.\s*'+c] for c in uppers]))

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
    boundaries = whiteSpace+":;?!"
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
    alltxt = body.itertext()
    for t in alltxt:
       txt += ' '+t 
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
    #if okLength(mlen):
    #    return res
    
    # then count the sentences separated by ','
    (klen,caps) = countSentence(txt,',')
    mklen = mediumLen(klen)
    mediumCap2 = len(filter(lambda x: x, caps))/float(len(caps))
    res.update({'rank' : 2,'Cleng' : mklen, 'caps' : mediumCap2})
    # returns rank 2, good sentences
    #if okLength(mklen):
#        return res

    # then count the sentences separated by capitalized words
    (xlen,_) = countSentence(txt,uppers)
    mxlen = mediumLen(xlen)
    res.update({'rank' : 3, 'Uleng' : mxlen, 'caps' : mediumCap1})
    # returns rank 3, ok sentenecs
    #if okLength(mxlen):
#       return res

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
