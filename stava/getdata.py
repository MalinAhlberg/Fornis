# -*- coding: utf-8 -*-
from extracttxt import *
from cc import norm,spellchecksmall
from xml.etree import ElementTree as etree
import collections
from collections import Counter
import printstats
import codecs
import re
import glob
import sys
import time


""" Output files, all words and their found variations are printed to
    outputWords summary data is printed to outputData """

outputStats = 'kast1'



""" sammanstall reads xml files and finds spelling variation of the text"""
def sammanstall():
    from readvariant import mkeditMap #,mkeditMap2
    files = ['colingeval/goodwordsall'] 
   # files = testfiles

    #hashd = readlex(oldlex2,old=True)
    hashd = readcorpuslex('colingeval/goodwordsall')

    edit,alpha = mkeditMap('trimap_small.txt',weigth=False)
    sys.stdout = codecs.open('ecoling5','w',encoding='utf-8')
    [getdata(fil,hashd,alpha,edit) for fil in files]

    print 'printed files',outputStats


""" Paths to testfiles """
testfiles1 = ['../filerX/SkaL.xml','../filerX/Erik-A.xml'
            ,'../filerX/AngDikt.xml','../filerX/Laek9.xml']
testfiles = glob.glob('testfiles/*xml')

""" Paths to lexicons """
oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
oldlex2 = (['schlyter.xml'
           ,'soederwall_main.xml'
           ,'soederwall_supp.xml'])

dalin    = ['../../Lexicon/dalin.xml']
smalllex = ['../scripts/littlelex.xml'] 
morflex  = ['../../Lexicon/good/lmf/fsv/fsv.xml'] 

""" getdata takes a xml file, a hashed lexicons and a set of allowed spelling
    variations and identifies spelling variations"""
def getdata(fil,hashd,alpha,edit):
    print fil
    #txt    = ''.join(gettext(fil))#'cristindom' #'villhonnugh' # # euangelio' #'euangelio' #'euangelio' 

    txt    = codecs.open(fil,'r',encoding='utf8').readlines()
    wds    = map(lambda x: x.split()[0],txt)
    #wds = [u'forbarmer'] #ärlighabiskopssätitlätkeysarlodouicus']
             # barochusmathirimiödhyrtthenna 


#    with codecs.open(fil,'r','utf8') as f:

#   txt    = ''.join(f.read()) 
#   wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}

    # look through all types, find spelling variation and create a dictionary of these
    t0 = time.clock()
    for (w,i) in typs.items():
      dic.update({w:spellchecksmall(w,hashd,alpha,edit)})
    print 'time',int(time.clock()-t0)

    # tab is a list of all words in the same order as in the text, mapped to
    # their spelling variation
# Behövs ej för coling eval    
#    tab = map(lambda w: (w,dic.get(w)),wds)
    
#    with codecs.open(outputStats,'a',encoding='utf8') as f:
#      f.write('\n'+fil+'\n'+printstats.printstat(tab))


""" calculate extracts data of how many types and tokens that could be found
    directly in the lexicon"""
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

"""Help function to readlexnormal"""
def insertnormal(d,form,lem):
    old = d.get(form)
    if old==None:
      lst = []
    else:
      lst = old
    d.update({form : [lem]+lst})

if __name__ == "__main__":

  sys.stdout = codecs.getwriter('utf8')(sys.stdout)
  sammanstall()

