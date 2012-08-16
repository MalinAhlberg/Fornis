# -*- coding: utf-8 -*-
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
  maxl = 1
  for line in lines:
    line = line.split('\t')
    #line = line.split(' ')
    #source_dest  = nytrans(line[0],line[1])
    source_dest  = trans(line[0],line[1])
    val  = int(float(line[2])*1000000) if weigth else int((-log(float(line[2])))/10*1000000)
    #if source_dest:
    #val  = int(float(line[3])*1000000) if weigth else int((-log(float(line[3])))/10*1000000)
    #for (x,y) in combinations(*source_dest):
    for (x,y) in combinations(*source_dest):
      editMap.update({(x,y):(len(x),len(y),val)})
      add(x,y,val,changeSet)
      if both:
        editMap.update({(y,x):(len(y),len(x),val)})
        add(y,x,val,changeSet)
      ml = max(len(x),len(y))
      if ml>maxl:
        maxl = ml
      

  return ((editMap,maxl),changeSet)


def mkeditMap2(fil):
  lines = codecs.open(fil,'r','utf8').readlines()
  editMap = {}
  changeSet = {}
  maxl = 1
  for line in lines:
    line = line.split(' ')
    source_dest  = nytrans(line[0],line[1])
    if source_dest:
      source,dest = source_dest
      val  = int((-log(float(line[3])))/10*1000000)
      editMap.update({source_dest:(len(source),len(dest),val)})
      add(source,dest,val,changeSet)
      ml = max(len(source),len(dest))
      if ml>maxl:
        maxl = ml
      

  return ((editMap,maxl),changeSet)


def nytrans(x,y):
  if x.startswith('_'):
    if y.startswith('_'):
     return (u'^'+x[1:],u'^'+y[1:])
  if x.endswith('_'):
    if y.endswith('_'):
     return (x[:1]+u'$',y[:1]+u'$')
  else:
    return x,y
  
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
