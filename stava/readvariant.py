import re
import codecs
from normalize import hashiso

def getvariant(fil):
  lines = codecs.open(fil,'r','utf8').readlines()
  d = {}
  for line in lines:
    line = re.sub('\^|\$','_',line).split()
    key  = line[0]
    val  = line[1]
    add(key,val,d)
    add(val,key,d)
  return d

def add(key,val,d):
    isokey = hashiso(key)
    isoval = hashiso(re.sub('_','',val))  # don't keep the end and start marks in val
    old  = d.get(isokey)
    newval = [isoval] if old is None else [isoval]+old
    d.update({isokey : newval})


    
