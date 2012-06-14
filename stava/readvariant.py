# -*- coding: utf_8 -*-
import re
import codecs
from normalize import hashiso
from math import log

""" This scripts reads a file of spelling variations
    (see lex_variation.txt) and creates a dictionary
    used by cc.py """
# not updated for use
#def getvariant(fil):
#  lines = codecs.open(fil,'r','utf8').readlines()
#  d = {}
#  for line in lines:
#    line = line.split()
#    key  = line[0]
#    val  = line[1]
#    add(key,val,d)
#    add(val,key,d)
#  return d
#
def add(key,var,val,d):
    isokey = hashiso(key)
    isoval = hashiso(var)
    #isoval = hashiso(re.sub('_','',val))  # don't keep the end and start marks in val
    old  = d.get(isokey)
    newval = [(isoval,val)] if old is None else [(isoval,val)]+old
    d.update({isokey : newval})


def mkeditMap(fil,both=False,weigth=True):
  lines = codecs.open(fil,'r','utf8').readlines()
  editMap = {}
  changeSet = {}
  for line in lines:
    line = line.split('\t')
    org,var  = trans(line[0],line[1])
    #var  = trans(line[1])
    val  = float(line[2]) if weigth else (-log(float(line[2])))/10
    for (x,y) in combinations(org,var):
      editMap.update({(x,y):(len(x),len(y),val)})
      add(x,y,val,changeSet)
      if both:
        editMap.update({(y,x):(len(y),len(x),val)})
        add(y,x,val,changeSet)
        

    #add((val,key,d) ska ej behövas
  return (editMap,changeSet)

def trans(x,y):
 if x=='_':
   return (['^','$'],['^'+y,y+'$'])
 if y=='_':
   return (['^'+x,x+'$'],['^','$'])
 return ([x],[y])

#def trans(x):
#  if x=='_':
#    return ['^','$']
#  else: return [x]

def combinations(xs,ys):
  return [(x,y) for y in ys for x in xs]
