# -*- coding: utf_8 -*-
from xml.etree import ElementTree as etree
import codecs
from normalize import normalize,iso,norm,hashiso
from cc import alphabet,getccs,getchanges
#import dl
from dltransl import edit_dist
import Queue
import threading

#TODO START the handeling of $^ vs _ gets different results. Which ones do we want?
# read and collect all text in xml. but we only get more by being less strict
def gettext(fil):
    xmls = codecs.open(fil,'r','utf8').read()
    tree = etree.fromstring(xmls)
    return tree.find('body').itertext()

# gather pairs of words from the text that could be variations of each other
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
          oks.append((w,cc,dist))
    print oks
      

# reads lexicons and a text and idenitfies spelling variations,
# using the lexicons as a standard
def lookup():
    from readvariant import getvariant
    txt    = ' '.join(list(gettext('../filerX/Albinus.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    a,_    = normalize(wds) 
    d      = readlex(['../scripts/lexiconinfo/newer/schlyter.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
    alpha  = getvariant('lex_variation.txt')
    oks    = []
    inlex  = []
    print 'will find ccs and rank'
    # TODO tråda här? blir ej snabbare!
    #queue = Queue.Queue(0)
    wds = set(wds)
    for w in wds:
    #  print w
    #  t = threading.Thread(target=spellcheckword,args=(w,d,alpha,a,oks,inlex,queue))
      #t.start()
      spellcheckword(w,d,alpha,a,oks,inlex)
    #for i in wds:
    #  a = queue.get()
    #  oks += a
    oks = sorted(set(oks),key= lambda (w,c,d,l): d)
    codecs.open('variant2','w',encoding='utf8').write(shownice(oks))
    codecs.open('inlex','w',encoding='utf8').write(shownice(inlex))

def spellcheckword(w,d,alpha,a,oks,inlex): #,queue):
  from math import fabs

  def getlemgram():
    res = d.get(hashiso(w))
    if res !=None:
      return res.get(w)
#  print w,getlemgram()
  lem = getlemgram()
  if lem==None:
    ccs    = []
    cc  = getchanges(w,d,alpha)
    #cc = []
    getccs((w,hashiso(w)),d,a,cc)
    ccs.append((w,set(cc)))
    # allowed dist should depend on wordlength?
    for (w,cc) in ccs:
      for (c,lem) in set(cc):
        if fabs(len(w)-len(c))<=len(w)/2:
          dist = edit_dist(w,c)
          if dist<2:
            oks.append((w,c,dist,lem))
          #   queue.put([(w,c,dist,lem)])
  else:
    inlex.append((w,lem))
 

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

if __name__ == "__main__":
   lookup()

def supertest():
    txt    = ' '.join(list(gettext('../filerX/Luk41SLundversion.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    print len(set(wds))
 
