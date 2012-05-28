# -*- coding: utf_8 -*-
from extracttxt import gettext,shownice,getLemgram,getWrittenforms
from normalize import norm
from xml.etree import ElementTree as etree
from collections import Counter
import codecs
import re
import glob


def sammanstall():
    files = glob.glob('../filerX/*xml')+glob.glob('../../filerXNy/*xml')
    d     = readlexnormal(oldlex) #dalin,old=True) #oldlex
    res = [getdata(fil,d) for fil in files]
    codecs.open('totresult','w',encoding='utf8').write(shownice(res))

oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
dalin = ['../../Lexicon/dalin.xml']

def getdata(fil,d):
    from readvariant import getvariant
    print fil
    txt    = ' '.join(list(gettext(fil)))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}
   # map(lambda (w,i): dic.update({w:(d.get(w),i)}),typs.items())

    map(lambda (w,i):  dic.update({w:spellcheckword(w,d,alpha,a)}),typs.items() # TODO find args for spellc
    #spelled = map(lambda (w,i): ,typs.items() 
    tab = map(lambda w: (w,dic.get(w)),wds)
    gw,gt,bw,bt = calculate(dic)
    res = 'good '+str(gw)+' ('+str(gt)+') bad '+str(bw)+' ('+str(bt)+')\n***\n'
 
    
    codecs.open('results','a',encoding='utf8').write('\n'+fil+' '+res+'\n'+shownice(tab))
    return (fil,gw,gt,bw,bt,gw+bw,gt+bt)


#TODO START this should do the same job as before but maybe also count how many spelling variants we have
# then we should print similair result files with overviewable data about spelling variants
def calculate(dic):
    oks,bads = [],[]
    bokstaver = u'\w|[åäöÅÄÖæÆøØÞþß]' 
    def count(w,r,i):
      if r==None:
        bads.append(i) 
      else:
        oks.append(i) 
    [count(w,r,i) for (w,(r,i)) in dic.items() if re.search(bokstaver,w.strip())]
#    good = len(filter(lambda x:x==1,res))
#    bad =  len(filter(lambda x:x==0,res))
    return (sum(oks),len(oks),sum(bads),len(bads))

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

