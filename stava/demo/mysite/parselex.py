# -*- coding: utf-8 -*-
#xml -> model
from xml.etree import ElementTree as etree
from textview.models import Lemgram,Variant
from django.db import models
import glob

#lex = ['../../testlex.xml']
lex = glob.glob('../../../../Lexicon/good/lmf/soederwall*/*xml')+['../../../../Lexicon/good/lmf/schlyter/schlyter.xml']

def readlex(files):
    for fil in files:
      s = open(fil,"r").read()
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem      = getLemgram(entry,old=True)
         #text = getInfo(entry)
#         print 'will add lemgram'
         lemref = addLemgram(lem)
         #lemref = addLemgram(lem,text[:200])
#         print 'added lemgram'
         forms  = getWrittenforms(entry)
         for form in forms:
           addWritten(form[:50],lemref)
#           print 'added one written'

 
def getInfo(entry):
  formrep = entry.find('Lemma').find('FormRepresentation')
  #pos     = getAtt(formrep,'partOfSpeech')
  sense   = entry.find('Sense')
  text    = ''
  if sense is not None:
    sdef = sense.find('Definition')
    text = getAtt(sense,'text')
  return ' '.join(text)

def addLemgram(lem):
  ls = Lemgram.objects.filter(lemgram=lem)
  if ls:
    l = ls[0]
  else:
    l = Lemgram(lemgram=lem) #, text=txt)
    l.save()
  return l
    
#  if len(ls)==1:
#    #print 'first text'
#    l = ls[0]
#    l.text += txt
#  else:
#    print 'second pos_text',txt
#    l = Lemgram(lemgram=lem, text=txt)
#    print 'have a lemgram',l
#  l.save()
#  print 'saved it'
#  return l

def addWritten(form,lemref):
  #print 'begin of add written'
  ws = Variant.objects.filter(form=form)
  if ws:
  #  print 'found a written'
    w = ws[0]
  else:
  #  print 'did not find a written'
    w = Variant(form=form)
    w.save()
  #print 'add lemref to written'
  w.lemgrams.add(lemref)
  w.save()
   
def getAtt(elem,val):
  res = []
  if not elem is None:
    for feat in elem:
        value = feat.get('att')
        if value == val:
           res.append(feat.get('val'))
  return res


def getLemgram(entry,old=False,morf=False):
    lemma = entry.find('Lemma')
    if old or morf:
      lemma  = lemma.find('FormRepresentation')
    for feat in lemma:
      value = feat.get('att')
      if value == 'lemgram':
        return feat.get('val')
            
def getWrittenforms(entry):
  forms  = entry.find('Lemma').findall('FormRepresentation')
  ws     = []
  for form in forms:
    writtens = getAtt(form,'writtenForm')
    ws += writtens
  return ws


