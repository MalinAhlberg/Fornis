# -*- coding: utf_8 -*-
from extracttxt import *
from cc import norm,spellchecksmall
from xml.etree import ElementTree as etree
from collections import Counter
import printstats
import codecs
import re
import glob

""" Output files, all words and their found variations are printed to
    outputWords summary data is printed to outputData """

outputStats = 'kast3'



""" sammanstall reads xml files and finds spelling variation of the text"""
def sammanstall():
    from readvariant import mkeditMap    
   #files = glob.glob('../filerX/*xml')+glob.glob('../filerXNy/*xml')
    files = testfiles #['testfiles/lilleSkaL'] #
    #files = ['testfiles/lilleSkaL'] 
   #hashd = readlex(morflex,morf=True)
   #hashd = readlex(smallex)
    hashd = readlex(oldlex2,old=True)
    #edit,alpha  = mkeditMap('lex_variation.txt',both=True)
    #edit,alpha = mkeditMap('char_variant.txt')
    #edit,alpha = mkeditMap('char_varsmallest.txt')
    #edit,alpha = mkeditMap('trimap_var.txt',weigth=False)
    edit,alpha = mkeditMap('trimap_small.txt',weigth=False)
    [getdata(fil,hashd,alpha,edit) for fil in files]
#    codecs.open(outputData,'w',encoding='utf8').write(shownice(res))
    print 'printed files',outputStats


""" Paths to testfiles """
testfiles1 = ['../filerX/SkaL.xml','../filerX/Erik-A.xml'
            ,'../filerX/AngDikt.xml','../filerX/Laek9.xml']
testfiles = glob.glob('testfiles/*xml')

""" Paths to lexicons """
oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
oldlex2 = (['../../Lexicon/schlyter.xml'
           ,'../../Lexicon/soederwall_ny/soederwall_main_NYAST.xml'
           ,'../../Lexicon/soederwall_ny/soederwall_supp_NYAST.xml'])

dalin    = ['../../Lexicon/dalin.xml']
smalllex = ['../scripts/littlelex.xml'] 
morflex  = ['../../Lexicon/good/lmf/fsv/fsv.xml'] 

""" getdata takes a xml file, a hashed lexicons and a set of allowed spelling
    variations and identifies spelling variations"""
def getdata(fil,hashd,alpha,edit):
    print fil
    txt    = ''.join(gettext(fil)) 
    wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}

    # look through all types, find spelling variation and create a dictionary of these
    map(lambda (w,i):  dic.update({w:(i,spellchecksmall(w,hashd,alpha,edit))}),typs.items()) 
    # tab is a list of all words in the same order as in the text, mapped to
    # their spelling variation
    tab = map(lambda w: (w,dic.get(w)),wds)
    
    with codecs.open(outputStats,'a',encoding='utf8') as f:
      f.write('\n'+fil+'\n'+printstats.printstat(tab))


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
  sammanstall()

