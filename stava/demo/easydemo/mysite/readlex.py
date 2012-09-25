# -*- coding: utf-8 -*-
from xml.etree import ElementTree as etree
import codecs
import re
import urllib

# Functions for reading xml lexicons into one dictionary
"""reads lexicons into a hased anagram dictionary:
     {wordForm : [(lemgram: {pos : string, gram : string,
                             hwtext : string, senses : [string]})]} """

def readlex(files):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      lexname = getname(fil)
      lexicon = etree.fromstring(s)
      entries = lexicon.find('Lexicon').findall('LexicalEntry')
      for entry in entries:
         forms = getWrittenforms(entry)
         for form in forms:
           insert(d,form,lexname,entry)
    return d

def test(word):
  site = 'http://spraakbanken.gu.se/ws/karp-sok?resurs=fsvm&wf='+word #+'&format=json'
  print 'calling kark',site
  f = urllib.urlopen(site)
  lexinfo = f.read()
  f.close()
  return readkarklex([lexinfo])
  
def readkarklex(xmls):
    d = {}
    for xml,lexname in xmls:
      lexicon = etree.fromstring(xml)
      divs = lexicon.findall('div')
      for div in divs:
        for entry in div.findall('LexicalEntry'):
         forms = getWrittenforms(entry)
         for form in forms:
           insert(d,form,lexname,entry)
    return d



def getLemgram(entry):
    lemma = entry.find('Lemma').find('FormRepresentation')
    for feat in lemma:
      if feat.get('att') == 'lemgram':
        return feat.get('val')
             
""" Returns all writtenForms of an entry """
def getWrittenforms(entry,old=False,morf=False):
    forms = entry.find('Lemma').findall('FormRepresentation') 
    return sum([getAttList(form,'writtenForm') for form in forms],[])

def insert(d,form,lexname,entry):
    formrep = entry.find('Lemma').find('FormRepresentation')
    pos     = ' '.join(set(getAttList(formrep,'partOfSpeech')))
    gram    = getAtt(formrep,'gram')
    hwtext  = getAtt(formrep,'hwtext')
    senses  = entry.findall('Sense')
    defs    = sum([sense.findall('Definition') for sense in senses  if sense is not None],[])
    senses  = [(i,getAtt(x,'text')) for i,x in enumerate(defs)]
    dentry  = {'pos' : pos, 'gram' : gram, 'hwtext' : hwtext, 'senses' : dict(senses)}
    d.setdefault(form,[]).append((getLemgram(entry),lexname,dentry))

def getname(fil):
  if re.search('schlyter',fil): 
    return 'Schlyter'
  if re.search('supp',fil): 
    return 'Soederwalls supplement'
  else:
    return 'Soederwall'

def getAtt(elem,val):
  return ' '.join(getAttList(elem,val))

def getAttList(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append(feat.get('val'))
    return res


def getthem():
  return readlex(['/home/malin/Spraak/Lexicon/good/lmf/schlyter/schlyter.xml'
                 ,'/home/malin/Spraak/Lexicon/good/lmf/soederwall/soederwall.xml'
                 ,'/home/malin/Spraak/Lexicon/good/lmf/soederwall_supp/soederwall_supp.xml'])
