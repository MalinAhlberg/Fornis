# -*- coding: utf_8 -*-
from xml.etree import ElementTree as etree
import codecs
from normalize import normalize,iso,norm,hashiso
from cc import alphabet,getccs,getchanges
#import dl
from dltransl import edit_distdebug

def gettext(fil):
    xmls = codecs.open(fil,'r','utf8').read()
    tree = etree.fromstring(xmls)
    return tree.find('body').itertext()

def writelex():
    txt    = ' '.join(list(gettext('../filerX/Albinus.xml')))
    wds    = txt.split()
    d,nwds = normalize(wds) # prints bu, frekvenslista and lex
    alpha  = alphabet(wds)
    oks    = []
    for (w,av) in nwds:
      ccs = getccs((w,av),d,alpha)
      # this should be done earlier? use rank in cc
      # instead we could look all proposals up in lexicon
      # here, and decide wether we want to keep word or not
      for (cc,i) in ccs:
        dist = dl.edit_dist(w,cc)
        if dist<3:
          oks += [(w,cc,dist)]
    print oks
      
      #calculatevariants(w,alpa,d)   # should get cc and rank them 

# TODO use set instead of list
def lookup():
    from readvariant import getvariant
    from math import fabs
    txt    = ' '.join(list(gettext('../filerX/Albinus.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    a,_    = normalize(wds) # prints bu, frekvenslista and lex
    d      = readlex(['../scripts/lexiconinfo/newer/schlyter.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
    alpha  = getvariant('lex_variation.txt')
    oks    = []
    inlex  = []
    print 'will find ccs and rank'
    # TODO tråda här?
    for w in set(wds):
      ccs    = []
      cc  = getchanges(w,d,alpha)
      getccs((w,hashiso(w)),d,a,cc)
      ccs += [(w,set(cc))]
      # TODO check that only allowed lex-var is made, nothing else
      # hv and a-e in dl
      # todo fix lemgram
      # allowed dist should depend on wordlength?
      for (w,cc) in ccs:
        for (c,lem) in set(cc):
          if c==w:  #exact copies are not considered
            inlex += [(w,lem)]
          elif fabs(len(w)-len(c))<=len(w)/2:
            dist = edit_distdebug(w,c)
          # TODO if a anagram is in lex, this word should still be considered
            if dist<2 and d.get(hashiso(w)) is None:
              oks += [(w,c,dist,lem)]
    oks = sorted(set(oks),key= lambda (w,c,d,l): d)
    codecs.open('variants','w',encoding='utf8').write(shownice(oks))
    codecs.open('inlex','w',encoding='utf8').write(shownice(inlex))

def shownice(xs):
    slist = ['\t'.join([unicode(w) for w in x]) for x in xs]
    s = "\n".join(slist)
    return s

# return dictionary {av : {form : lemma}}
def readlex(files):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem = getLemgram(entry)
         forms  = getWrittenforms(entry)
         for form in forms:
           insert(d,form,lem)
    return d

def getLemgram(entry):
    lemma = entry.find('Lemma')
    for feat in lemma:
      value = feat.get('att')
      if value == 'lemgram':
        return feat.get('val')
            
def getWrittenforms(entry):
    lemma = entry.find('Lemma')
    forms  = lemma.findall('FormRepresentation')
    ws     = []
    for form in forms:
      writtens = getAtt(form,'writtenForm')
      ws += writtens
    return ws

def getAtt(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append(feat.get('val'))
    return res

def insert(d,form,lem):
    key = sum([iso(c) for c in form])
    old = d.get(key)
    if old!=None:
      old.update({form:lem})
    else:
      d.update({key : {form : lem}})


lookup()

def supertest():
    txt    = ' '.join(list(gettext('../filerX/Luk41SLundversion.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    print len(set(wds))
 
