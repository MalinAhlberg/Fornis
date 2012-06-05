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


    
