# -*- coding: utf_8 -*-
from xml.etree import ElementTree as etree
import codecs
from cc import alphabet,getccs,getchanges
from dltransl import edit_dist
import Queue
import threading

""" reads and collects all text in xml """
def gettext(fil):
    xmls = codecs.open(fil,'r').read()
    tree = etree.fromstring(xmls)
    elems  = tree.find('body')
    for e in elems.iter():
      if e.tag in ['para','section']:
        old  = e.text or ''
        e.text = ' '+old
    return elems.itertext()

"""
combines rules with 'normal' spelling variation. applies edit distance
spellcheckword(word,hashlexicon,rules for variations,alphabet of common hash-grams)
returns (False,(word,lemgram)) if the word is in the lexicon
returns (True,(word,variant,distance,lemgram)) if variants are found
returns (False,None) if nothing interesting is found
"""
def spellcheckword(w,d,rules,a): 

  lem = getlemgram(d,w)
  if lem==None:
    ccs    = []
    cc  = getchanges(w,d,rules)
    getccs((w,hashiso(w)),d,a,cc)
    ccs.append((w,set(cc)))
    # allowed dist should depend on wordlength?
    res = getvariant(ccs)
    if res:
      return (True,res)
  else:
    return (False,(w,lem))

  # False,None implies it was in dict but we didn't get good spelling variants
  return (False,None)

"""
 rule based spell checking. applies edit distance
 spellchecksmall(word,hashlexicon,rules for variations)
 returns (False,(word,lemgram)) if the word is in the lexicon
 returns (True,(word,variant,distance,lemgram)) if variants are found
 returns (False,None) if nothing interesting is found
"""
def spellchecksmall(w,d,alpha):
  lem = getlemgram(d,w)
  if lem==None:
    ccs = [(w,getchanges(w,d,alpha))]
    res = getvariant(ccs)
    if res:
      return (True,res)
  else:
    return (False,(w,lem))
  return (False,None)
 
""" finds the lemgram of a word in a lexicon of anagram values"""
def getlemgram(d,w):
    res = d.get(hashiso(w))
    if res !=None:
      return res.get(w)
 
""" Examines a set of words and their variations and picks
    the ones that has an accepteble edit distance (2)
    returns a list of (word,variation,edit distance,lemgram)"""
def getvariant(ccs):
  from math import fabs
  var = []
  for (w,cc) in ccs:
    for (c,lem) in set(cc):
      if fabs(len(w)-len(c))<=len(w)/2:
        dist = edit_dist(w,c)
        if dist<2:
          var.append((w,c,dist,lem))
  var.sort(key=lambda (w,c,dist,lem): dist)
  return var

"""Help function for pretty printing"""
def shownice(xs):
    slist = ['\t'.join([unicode(w) for w in x]) for x in xs]
    s = "\n".join(slist)
    return s

# Functions for reading an xml lexicon
"""reads a lexicon into a hased anagram dictionary.
   If old is set to True, lemgram is supposed to be located inside
   FormRepresentation, otherwise directly in Lemma """
def readlex(files,old=False):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem = getLemgram(entry,old)
         forms  = getWrittenforms(entry,old)
         for form in forms:
           insert(d,form,lem)
    return d

""" Returns the lemgram of an entry
    If old is set to True, lemgram is supposed to be located inside
    FormRepresentation, otherwise directly in Lemma """
def getLemgram(entry,old=False):
    lemma = entry.find('Lemma')
    if old:
      lemma  = lemma.find('FormRepresentation')
    for feat in lemma:
      value = feat.get('att')
      if value == 'lemgram':
        return feat.get('val')
            
""" Returns all writtenForms of an entry """
def getWrittenforms(entry,old=False):
    lemma = entry.find('Lemma')
    container = 'FormRepresentation'
    forms  = lemma.findall(container) 
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
def insert(d,form,lem):
    key = sum([iso(c) for c in form])
    old = d.get(key)
    if old!=None:
      old.update({form:lem})
    else:
      d.update({key : {form : lem}})

