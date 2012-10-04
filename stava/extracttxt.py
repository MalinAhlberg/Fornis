# -*- coding: utf-8 -*-
from xml.etree import ElementTree as etree
import codecs
from cc import alphabet,getchanges,iso,hashiso
import Queue
import threading
import re

""" reads and collects all text in xml """
def gettext(fil):
    xmls = codecs.open(fil,'r').read()
    tree = etree.fromstring(xmls)
    elems  = tree.find('body')
    for e in elems.iter():
#    for e in elems.getiterator():
      if e.tag in ['para','section']:
        old  = e.text or ''
        e.text = ' '+old
    return elems.itertext()

""" reads a file *.token.word produced by the korp-import chain """
def getkorptext(fil):
   wds = []
   with codecs.open(fil,'r',encoding='utf-8') as f:
     for line in f:
       wds.append(line.split()[1])
   return wds

""" finds the lemgram of a word in a lexicon of anagram values"""
def getlemgram(d,w):
    res = d.get(hashiso(w))
    if res !=None:
      return res.get(w)


"""Help function for pretty printing"""
def shownice(xs,t='\t',n='\n'):
    slist = [t.join([unicode(w) for w in x]) for x in xs]
    s = n.join(slist)
    return s

# Functions for reading an xml lexicon
"""reads lexicons into a hased anagram dictionary:
     {hash : {wordForm : [(lemgram, lexiconname)]}}
   If old is set to True, lemgram is supposed to be located inside
   FormRepresentation, otherwise directly in Lemma
   morf indicates if the lexicon is a morfology file.. savest not to use"""
def readlex(files,old=False,morf=False):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      nicefil = getShortFile(fil)
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem = getLemgram(entry,old,morf)
         forms  = getWrittenforms(entry,old,morf)
         for form in forms:
           insert(d,form,lem,nicefil)
    return d

def readcorpuslex(fil):
    ss = codecs.open(fil,"r",encoding='utf8').readlines()
    d = {}

    for line in ss:
       xs = line.split()
       insert(d,xs[0],'',xs[1:])
       #for source in xs[1:]:
    return d





""" Returns the lemgram of an entry
    If old is set to True, lemgram is supposed to be located inside
    FormRepresentation, otherwise directly in Lemma """
def getLemgram(entry,old=False,morf=False):
    lemma = entry.find('Lemma')
    if old or morf:
      lemma  = lemma.find('FormRepresentation')
    for feat in lemma:
      value = feat.get('att')
      if value == 'lemgram':
        return feat.get('val')
            
""" Returns all writtenForms of an entry """
def getWrittenforms(entry,old=False,morf=False):
    #lemma = entry.find('Lemma')
    if morf:
      container = 'WordForm'
    else:
      container = 'FormRepresentation'
      entry = entry.find('Lemma')
    forms  = entry.findall(container) 
    ws     = []
    for form in forms:
      writtens = getAtt(form,'writtenForm')
      ws += writtens
    return ws

""" Help function for reading lexicon
    Returns the value (if any) of attribute val in elem
    <hej> <feat att="djur" val="katt">" </hej>
    --> ["katt"]
"""
def getAtt(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append(feat.get('val'))
    return res

"""Help function to readlexnormal
   inserts lem in the dictionary lem in the dictionary d"""
def insert(d,form,lem,fil):
    key = sum([iso(c) for c in form])
    d.setdefault(key,{}).setdefault(form, []).append((lem,fil))


def getShortFile(fil):
   if re.search('schlyter',fil):
     return 'Sch'
   if re.search('main',fil):
     return 'SoeM'
   if re.search('supp',fil):
     return 'SoeS'
   if re.search('fsv',fil):
     return 'fsv'
   else:
     return '?'
