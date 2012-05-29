# -*- coding: utf_8 -*-
from extracttxt import gettext,shownice,getLemgram,getWrittenforms,readlex,spellchecksmall
from normalize import norm,normalize
from xml.etree import ElementTree as etree
from collections import Counter
import codecs
import re
import glob


def sammanstall():
    from readvariant import getvariant
    files = glob.glob('../filerX/*xml')+glob.glob('../../filerXNy/*xml')
    #d     = readlexnormal(oldlex) #dalin,old=True) #oldlex
    hashd = readlex(oldlex)#dalin,old=True) #oldlex
    alpha  = getvariant('lex_variation.txt')
    res = [getdata(fil,hashd,alpha) for fil in files]
    codecs.open('totresultAll','w',encoding='utf8').write(shownice(res))

oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
dalin = ['../../Lexicon/dalin.xml']

def getdata(fil,hashd,alpha):
    from readvariant import getvariant
    print fil
    txt    = ' '.join(list(gettext(fil)))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}
    ## map(lambda (w,i): dic.update({w:(d.get(w),i)}),typs.items())

    map(lambda (w,i):  dic.update({w:(i,spellchecksmall(w,hashd,alpha))}),typs.items()) # TODO find args for spellc
    ##spelled = map(lambda (w,i): ,typs.items() 
    #tab = map(lambda w: (w,dic.get(w)),wds)
    gw,gt,bw,bt,vw,vt = calculate(dic)
    #res = 'good '+str(gw)+' ('+str(gt)+') bad '+str(bw)+' ('+str(bt)+')\n***\n'
 
    
    #codecs.open('resultsAll','a',encoding='utf8').write('\n'+fil+' '+res+'\n'+shownice(tab))
    return (fil,gw,gt,bw,bt,vw,gw+bw+vw,gt+bt+vt)


#TODO START this should do the same job as before but maybe also count how many spelling variants we have
# Should print similar result files with overviewable data about spelling variants
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
#   [count(w,r,i) for (w,(r,i)) in dic.items() if re.search(bokstaver,w.strip())]
#    good = len(filter(lambda x:x==1,res))
#    bad =  len(filter(lambda x:x==0,res))
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

