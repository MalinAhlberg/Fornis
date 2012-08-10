# -*- coding: utf-8 -*-
#txt -> model
from textview.models import Lemgram,WrittenForm,Word
from django.db import models

def parsemap(fil):
  ss = open(fil,"r").readlines()
  for line in ss:
    wds = line.split()
    if wds:
      lemref = addWord(wds)

def addWord(wds):
  word = wds[0]
  w = Word(word= word)
  w.save()
  print 'saved word'
  for variant in wds[1:]:
    vs = WrittenForm.objects.filter(form=variant)
    print 'vs',vs
    for v in vs:
      print 'v',v
      w.variants.add(v)
      print 'added!!'
  print 'added variants to word'
  w.save()

 
