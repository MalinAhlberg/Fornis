# -*- coding: utf_8 -*-
import re
import os
import glob
import codecs
from xml.etree import ElementTree as etree
from xmlindent import indent

""" Various tools for reading and handeling dictionaries """


""" read file and return list of entries and reference to the whole lexicon """
def readIt(fil):
     s = codecs.open(fil,"r").read()
     lexicon = etree.fromstring(s)
     indent(lexicon)
     lex     = lexicon.find('Lexicon')
     entries = lex.findall('LexicalEntry')
     return (entries,lexicon)

""" lexical entry -> form representation      """
def getFormRepresentation(entry):
    lemma = entry.find('Lemma')
    form  = lemma.find('FormRepresentation')
    return form

""" lexical entry -> (pos-tag, element containing pos-tag) """
def getTag(entry,old=False):
    if old:
      lemma  = getFormRepresentation(entry)
    else:
      lemma = entry.find('Lemma')
    lems  = getAtt(lemma,lemgram)
    return extractTag(lems)

""" lem -> (pos-tag, element containing pos-tag) """
def extractTag(lem):
    if lem is not None:
        (tag,elem) = lem[0]
        return (tag.split('.')[2],elem)
    else: return (None,None)

""" lexical entry -> lemgram """
def getLem(entry,old=False):
    if old:
      lemma  = getFormRepresentation(entry)
    else:
      lemma = entry.find('Lemma')
    lems  = getAtt(lemma,lemgram)
    return extractLem(lems)

""" lem -> lemgram-id """
def extractLem(lem):
    if lem == []: print 'woo!',etree.tostring(lem)
    if lem is not None:
        (tag,elem) = lem[0]
        return tag
    else: return ""

# TODO entry -> sense_id,ref
def getSenseid(entry):
  sensids = []
  senses  = entry.findall('Sense')
  for sense in senses:
    if sense is not None:
      sensids.append((sense.get('id'),sense))
  return sensids
 

""" gets the value of 'val' in 'elem' 
    returns pair (value,reference)"""
def getAtt(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append((feat.get('val'),feat))
    return res

""" gets the reference the element in 'elem' which has value 'val'"""
def getAttRef(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res += [feat]
    return res

""" gets triples of children. elem -> (att,val,reference) """
def getAll(elem,skip=[]):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value not in skip:
             res.append((value,feat.get('val'),feat))
    return res
 
""" lookup word in lex. if the dictionary has ints as values,
    the Nothing-value (Null) is 0, otherwise [] """
def lookupLex(word,lex):
    lem = re.sub('\*|\?','',word)
    nullvalue = 0 if type(lex.values()[0])==int else []
    res = lex.get(lem) if lex.has_key(lem) else nullvalue
    return (lem,res)
 
soederwall_main = '../../Lexicon/soederwall_ny/soederwall_main_NYAST.xml'
soederwall_supp = '../../Lexicon/soederwall_ny/soederwall_supp_NYAST.xml'
schlyter        = '../../Lexicon/schlyter.xml'
currentfile= schlyter
 
allfiles = [soederwall_main, soederwall_supp, schlyter]


""" reads lexicons and creates on big dictionary """
def mkLex(keeppos=True,files=allfiles,numbers=False,senseId=False,meld=False,old=False):
    if len(files)==0: return {}
    allentries = []
    lex = {}
    if type(files[0]) == type('fil'):
      print 'reading files'
      print 'making lexicon'
      for fil in files: 
        entries,_ = readIt(fil) 
        allentries.append(entries)
    else:
      allentries = files
    for entry in allentries:
      lem     = getLem(entry,old)
      lemgram = re.sub('\*|\?','',lem)
      if not keeppos:
        lem = lem.split('.')[0]
      pos,_ = getTag(entry,old)
      lem1 = lem if not meld else re.sub('\*|\?','',lem)
      standard  = [{"form": lem,"pos" : pos, 'lemgram' : lemgram}] #"file" : fil, 
      attr  = 1 if numbers else standard
      insert(lex,lem1,attr)
      if senseId:
         map(lambda (ids,s): insert(lex,re.sub('\*|\?','',ids),attr), getSenseid(entry))
    print 'lexicon complete'
    return lex

""" insert(dictionary,key,value)
    inserts {value : number of occurences} in key in dic"""
def insert(d,k,standard):
    old = d.get(k)
    if old!=None:
      standard = old+standard
    d.update({k:standard})
 
""" change this according to what kind of lexicon we're using """
lemgram ='lemgram' # 'lem' # 
