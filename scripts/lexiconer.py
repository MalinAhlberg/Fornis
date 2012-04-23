# -*- coding: utf_8 -*-
import re
import os
import glob
from xml.etree import ElementTree as etree

def readIt(fil):
     s = open(fil, "r").read()
     lexicon = etree.fromstring(s)
     lex     = lexicon.find('Lexicon')
     entries = lex.findall('LexicalEntry')
     for entry in entries: 
         (tag,elem) = getTag(entry)
         print tag
         if not tag or tag =='e':
            setNewTag(elem,entry)
     print etree.tostring(lex)

            
     
       
def getTag(entry):
    lemma = entry.find('Lemma')
    form  = lemma.find('FormRepresentation')
    lems  = getAtt(form,'lem')
    if lems:
        (tag,elem) = lems[0]
        return (tag.split('.')[2],elem)
    else: return (None,None)

def setNewTag(elem,entry):
    sense = entry.find('Sense')
    form  = sense.find('Definition')
    txt   = getAtt(form,'text')
    for (t,_) in txt:
        if isNoun(t):
           print 'a noun!'
           old = elem.get('val')
           elem.set('val',re.sub('\.\.e\.','..nn.',old))

def isNoun(t):
  return t.startswith('n.') or t.startswith('f.') or t.startswith('m.')

def getAtt(elem,val):
    res = []
    for feat in elem:
        value = feat.get('att')
        if value == val:
           res.append((feat.get('val'),feat))
    return res
    
