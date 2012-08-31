# -*- coding: utf-8 -*-
#txt -> model
#token ::: dist, edits, variant, lemgrams ^^ variant dist -> model
from textview.models import Lemgram,Variant,Word
from django.db import models

def parsemap(fil):
  ss = open(fil,"r").readlines()
  for line in ss:
    if line.strip():
      wds = line.split(':::')
      if wds:
        lemref = addWord(wds)

def addWord(wds):
  word = wds[0].strip()
  w = Word(word= word,distance1=0,distance2=0,distance3=0)
  print 'created word'
  print 'wds',wds
  variants = wds[1].strip().split('^^')
  print 'variants',variants
  for i,vlist in enumerate(variants):
    print 'will split',vlist,'at ,',i
    vvs = vlist.split(',')
    variant = vvs[2]
    print 'variant to lookup',variant
    vs = Variant.objects.filter(form=variant)
    print 'vs',vs
    if vs:
    #for v in vs:
      print 'v',vs[0]
      setvariant(w,i,vs[0])
      #variantX.add(vs[0])
      print 'added!!'
      setdistance(w,i,vvs[0])
      print 'added',vs[0],vvs[0],'to',w
      print 'added variants to word'
    else:
      print 'error in variants' 
    print w
    w.save()

 
def setvariant(w,i,v):
  if i==0: w.variant1 = v
  if i==1: w.variant2 = v
  w.variant3 = v
 
def setdistance(w,i,d):
  if i==0:  w.distance1 = d
  if i==1:  w.distance2 = d
  w.distance3 = d


