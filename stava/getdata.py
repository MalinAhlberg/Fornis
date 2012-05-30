# -*- coding: utf_8 -*-
from extracttxt import gettext,shownice,getLemgram,getWrittenforms,readlex,spellchecksmall,spellcheckword
from normalize import norm,normalize
from xml.etree import ElementTree as etree
from collections import Counter
import codecs
import re
import glob

outputWords = 'smalltestallmar'
outputData  = 'smalltestdatamar'

def sammanstall():
    from readvariant import getvariant
    #files = glob.glob('../filerX/*xml')+glob.glob('../filerXNy/*xml')
    files = glob.glob('../filerX/Ap*xml')+glob.glob('../filerX/Mar*Lund*xml')
    hashd = readlex(oldlex)#dalin,old=True) #oldlex
    alpha  = getvariant('lex_variation.txt')
    res = [getdata(fil,hashd,alpha) for fil in files]
    codecs.open(outputData,'w',encoding='utf8').write(shownice(res))

oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
dalin =  ['../../Lexicon/dalin.xml']

def getdata(fil,hashd,alpha):
    from readvariant import getvariant
    print fil
    txt    = ''.join(list(gettext(fil)))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}
    a,_    = normalize(wds) #remove if using small spellcheck

    map(lambda (w,i):  dic.update({w:(i,spellcheckword(w,hashd,alpha,a))}),typs.items()) 
    tab = map(lambda w: (w,dic.get(w)),wds)
    gw,gt,bw,bt,vw,vt = calculate(dic)
    res = 'good '+str(gw)+' ('+str(gt)+') bad '+str(bw)+' ('+str(bt)+')'+'variations '+str(vw)+' ('+str(vt)+')\n***\n'
 
    
    codecs.open(outputWords,'a',encoding='utf8').write('\n'+fil+' '+res+'\n'+shownice(tab))
    return (fil,gw,gt,bw,bt,vw,vt,gw+bw+vw,gt+bt+vt)


def calculate(dic):
    oks,bads,var = [],[],[]
    bokstaver = u'\w|[åäöÅÄÖæÆøØÞþß]' 
    def count(w,i,(v,args)):
       if v:
        var.append(i)
       elif args==None:
        bads.append(i) 
       else:
        oks.append(i) 
    [count(w,i,args) for (w,(i,args)) in dic.items() if re.search(bokstaver,w.strip())]
    return (sum(oks),len(oks),sum(bads),len(bads),sum(var),len(var))

def readlexnormal(files,old=False):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem    = getLemgram(entry,old)
         forms  = getWrittenforms(entry,old)
         for form in forms:
           insertnormal(d,form,lem)
    return d

def insertnormal(d,form,lem):
    old = d.get(form)
    if old==None:
      lst = []
    else:
      lst = old
    d.update({form : [lem]+lst})

sammanstall()
