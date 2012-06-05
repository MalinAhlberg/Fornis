# -*- coding: utf_8 -*-
import extracttxt 
from xml.etree import ElementTree as etree
from collections import Counter
import codecs
import re
import glob

""" Output files, all words and their found variations are printed to
    outputWords summary data is printed to outputData """

outputWords = 'newtestkastall2' #'bibsmalltestall'
outputData  = 'newtestkastdata2' #'bibsmalltestdata'

""" sammanstall reads xml files and finds spelling variation of the text"""
def sammanstall():
    from readvariant import getvariant
    #files = glob.glob('../filerX/*xml')+glob.glob('../filerXNy/*xml')
    #files = glob.glob('../filerX/Ap*xml')+glob.glob('../filerX/Mar*Lund*xml')
    files = glob.glob('../filerX/Mar41*Lund*xml')
    hashd = readlex(oldlex)#dalin,old=True) #oldlex
    alpha  = getvariant('lex_variation.txt')
    res = [getdata(fil,hashd,alpha) for fil in files]
    codecs.open(outputData,'w',encoding='utf8').write(shownice(res))
    print 'printed files',outputWords,outputData

""" Paths to lexicons """
oldlex = (['../scripts/lexiconinfo/newer/schlyter.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
         ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
dalin =  ['../../Lexicon/dalin.xml']

""" getdata takes a xml file, a hashed lexicons and a set of allowed spelling
    variations and identifies spelling variations"""
def getdata(fil,hashd,alpha):
    from readvariant import getvariant
    print fil
    txt    = ''.join(gettext(fil)) 
    wds    = map(lambda x: norm(x).lower(),txt.split())
    typs   = Counter(wds)
    dic = {}
    #a = alphabet(wds)       #remove if using small spellcheck

    # look through all types, find spelling variation and create a dictionary of these
    map(lambda (w,i):  dic.update({w:(i,spellchecksmall(w,hashd,alpha))}),typs.items()) 
    # tab is a list of all words in the same order as in the text, mapped to
    # their spelling variation
    tab = map(lambda w: (w,dic.get(w)),wds)
    # calculate statistics about the success rate
    gw,gt,bw,bt,vw,vt = calculate(dic)
    res = ' '.join(['good',str(gw),'(',str(gt),') bad',str(bw),'(',str(bt)
                   ,')','variations',str(vw),'(',str(vt),')\n***\n'])
    
    # print the text where each word is mapped to its variations
    codecs.open(outputWords,'a',encoding='utf8').write('\n'+fil+' '+res+'\n'+shownice(tab))
    return (fil,gw,gt,bw,bt,vw,vt,gw+bw+vw,gt+bt+vt)

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

################################################################################
# Not used
################################################################################

"""reads a lexicon into a 'normal' dictionary.
   If old is set to True, lemgram is supposed to be located inside
   FormRepresentation, otherwise directly in Lemma """
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
