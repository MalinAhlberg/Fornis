# -*- coding: utf_8 -*-
import re

""" Normalization functions"""

""" normalize(words) returns a pair
    ({hashedvalue : {word : number of occurences}}, set of normalized words)
"""
def normalize(wds):
    d = {}
    normwds = set([])
    for w in wds:
       neww = norm(w)
       key = hashiso(neww)
       insert(d,key,neww)
       normwds.add((neww,key))  

    return (d,normwds)

""" insert(dictionary,key,value)
    inserts {value : number of occurences} in key in dic"""
def insert(d,k,val):
    old = d.get(k)
    i   = 0
    if old!=None:
      j = old.get(val)
      if j!=None:
        # ska aldrig vara None
        i = j
      old.update({val:i+1})
    else:
      d.update({k : {val : 1}})
    
def prettyprint(d):
    open('bu','w').write(str(d))

def iso(c):
  v = 0
  if c.isalpha() or c in bokstaver:
    v = ord(c.lower())
  return pow(v,5)

def hashiso(w):
    return sum([iso(c) for c in w])
  
def norm(w):
    return re.sub(u'[^\w'+bokstaver+']','',w)

bokstaver = u'åäöÅÄÖæÆøØÞþß^$' # obs ^ and $ here to mark end beginning of words
  
#normalisera:
#  gå igenom allt
#  sätt alfabet (alla små bokstäver) key(w) = sum [(iso c)^n | c <- w] (n = 5)
#  normalisera...
#  bygg frekvenslista, räkna bort punkter osv


