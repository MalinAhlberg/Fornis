# -*- coding: utf_8 -*-
import re
import os
import glob
import codecs
from xml.etree import ElementTree as etree

def readIt(fil):
     s = open(fil, "r").read()
     lexicon = etree.fromstring(s)
     lex     = lexicon.find('Lexicon')
     entries = lex.findall('LexicalEntry')
     return (entries,lexicon)
    
def references():
    (entries,lex) = readIt('../../Lexicon/schlyter.xml')
    lst = []
    saves = False # True

    for entry in entries: 
        (pos,l) = getTag(entry)
        # if it is has an e tag, try to fix it
        if pos == 'e':
          print 'tag is e!'
          ref = findReference(l,entry,entries,save=saves)
          if ref is not None: lst.append((l,ref))

    def format(lst):
        ss = ''
        for (a,b) in lst:
            ss += a+'\t'+b+'\n'
        return ss
    if saves:
      open('testRef.xml','w').write(etree.tostring(lex,encoding='utf-8'))
    codecs.open('refs2.txt','w','utf-8').write(format(lst))
         


def makeTags():
    (entries,lex) = readIt('../../Lexicon/schlyter.xml')
    counter =  []
    for entry in entries: 
        (tag,elem) = getTag(entry)
        if not tag or tag =='e':
           setNewTag(elem,entry,counter)
    open('testL.xml','w').write(etree.tostring(lex,encoding='utf-8'))
    print len(counter)

# lexical entry -> form representation       
def getFormRepresentation(entry):
    lemma = entry.find('Lemma')
    form  = lemma.find('FormRepresentation')
    return form

# lexical entry -> (pos-tag, element containing pos-tag)
def getTag(entry):
    form  = getFormRepresentation(entry)
    lems  = getAtt(form,'lem')
    return extractTag(lems)

# lem -> (pos-tag, element containing pos-tag)
def extractTag(lem):
    if lem is not None:
        (tag,elem) = lem[0]
        return (tag.split('.')[2],elem)
    else: return (None,None)

# check if there is unmatched paranthesis in hwtext
def checkHW(fil):
    (entries,_) = readIt('../../Lexicon/schlyter.xml')
    for entry in entries: 
         findHW(entry)

# lexical entry -> print if there's unmatched paranthesis
def findHW(lem):
    form = getFormRepresentation(lem)
    lems  = getAtt(form,'hwtext')
    (l,_) = getAtt(form,'lem')[0]
    for (hw,x) in lems:
        #print hw
        if countP(hw)!=0:
          print hw
          print l
     
def findReference(lem,entry,lex,save=False):
   # kolla om det står se i Sense -Definition - text
    sense  = entry.find('Sense')
    if not sense is None:
      info   = sense.find('Definition')
      if not info is None:
        texts  = getAtt(info,'text')
        for (txt,elem) in texts:
            words = txt.strip(' .').split(',')
             # isf slå upp ord (liten bokstav), om det bara finns ett alternativ
            if words and words[0].startswith('se ') and len(words)==1:
              lems = lookup(normalize(words[0]),lex,'writtenForm') # writtenform also for multiwords?
              # finns det bara en, visa den
              if len(lems)==1:
                (pos,_) = getTag(lems[0])
                #print 'got tag',pos
                if pos != 'e':
                   (reflem,_) = getAtt(getFormRepresentation(lems[0]),'lem')[0]
                   if save:
                     print 'saving',pos
                     lem.set('val',re.sub('\.\.e\.','..'+pos+'.',lem.get('val')))
                   return reflem
                else: print 'refererence to "e"',lems[0],txt
              else: print 'too many or few references',lems,txt
            elif words and words[0]=='se': 
              print 'bad reference',txt

def normalize(words):
    return (words[3:]).lower()  # remove 'se '
    #return re.sub(' ','_',word.lower())

def lookup(e,lex,typ):
    #print 'lookup',e
    res = []
    for entry in lex:
        form = getFormRepresentation(entry)
        eres = getAtt(form,typ)
        for (txt,elem) in eres:
            if txt==e:
              #print 'a match!',txt
              res.append(entry)
    return res



def setNewTag(elem,entry,counter):
    form = getFormRepresentation(entry)
    (l,_) = getAtt(form,'lem')[0]
    txt   = getAtt(form,'gram')
    old = elem.get('val')
    for (t,_) in txt:
        if isNoun(t):
           print 'nn',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..nn.',old))
        if isPrep(t):
           print 'prep',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..pp.',old))
        if isAdj(t):
           print 'adj',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..av.',old))
        if isVerb(t):
           print 'vb',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..vb.',old))
        if isAdv(t):
           print 'adv',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..ab.',old))
        if isConj(t):
           print 'conj',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..kn.',old))

# only in beginning of string? other word classes
# 'se Xxx'
def isNoun(t):
  return t.startswith('n.') or t.startswith('f.') or t.startswith('m.')
def isPrep(t):
  return t.startswith(u'præp.')
def isAdj(t):
  return t.startswith('adj.')
def isAdv(t):
  return t.startswith('adv.')
def isVerb(t):
  return t.startswith('v.')
def isConj(t):
  return t.startswith('conj.')

def getAtt(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append((feat.get('val'),feat))
    return res
    
# count number of paranthesis
def countP(w):
   i=0
   for c in w:
       if c=='(':
         i = i+1
       if c==')':
         i = i-1
   return i              

