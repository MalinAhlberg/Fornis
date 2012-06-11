# -*- coding: utf_8 -*-
import re
import codecs
from normalize import hashiso

""" This scripts reads a file of spelling variations
    (see lex_variation.txt) and creates a dictionary
    used by cc.py """

def getvariant(fil):
  lines = codecs.open(fil,'r','utf8').readlines()
  d = {}
  for line in lines:
    line = line.split()
    key  = line[0]
    val  = line[1]
    add(key,val,d)
    add(val,key,d)
  return d

def add(key,val,d):
    isokey = hashiso(key)
    isoval = hashiso(val)
    #isoval = hashiso(re.sub('_','',val))  # don't keep the end and start marks in val
    old  = d.get(isokey)
    newval = [isoval] if old is None else [isoval]+old
    d.update({isokey : newval})


def mkeditMap(fil):
  lines = codecs.open(fil,'r','utf8').readlines()
  editMap = {}
  changeSet = {}
  for line in lines:
    line = line.split('\t')
    org  = trans(line[0])
    var  = trans(line[1])
    val  = line[2]
    for (x,y) in combinations(org,var):
      editMap.update({(x,y):(1,1,float(val))})
      add(x,y,changeSet)

    #add((val,key,d) ska ej behövas
  return (editMap,changeSet)

def trans(x):
  if x=='_':
    return "^$"
  else: return x

def combinations(xs,ys):
  return [(x,y) for y in ys for x in xs]
