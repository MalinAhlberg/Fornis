# -*- coding: utf-8 -*-
from replacemap import replsX
from itertools import product
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

""" calculates the distance """
""" string1 , string2, dictionary of rules, maximum n-gram length """
def edit_dist(s1, s2,rules=replsX,n=3):
    s1 = '^'+s1+'$'
    s2 = '^'+s2+'$'
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    d[(-1,-1)] = 0
    for i in xrange(0,lenstr1):
        d[(i,-1)] = i+1
    for j in xrange(0,lenstr2):
        d[(-1,j)] = j+1
 
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            d[(i,j)] = replaceX(s1,i,s2,j,d,rules,n)
            
    res = d[lenstr1-1,lenstr2-1]
    return res

""" replacements """
def replaceX(s1,i,s2,j,d,rules,n):
  def replace1(s1,s2,i,j):
    xs = []
    for (a,b) in product((s1[-x:] for x in xrange(1,n+1)),(s2[-x:] for x in xrange(1,n+1))):
      val = rules.get((a,b),None) 
      if val:
        xs.append(d[(i-val[0],j-val[1])]+val[2])
    return xs
    
  same = issame(s1[i],s2[j])
  xs = replace1(s1[:i+1],s2[:j+1],i,j)
  return min(xs+[d[i-1,j-1]+same])
  


def issame(a,b):
  if a==b:
    return 0
  if a in vow and b not in vow:
    return 3000000
  return 1000000
  
dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

