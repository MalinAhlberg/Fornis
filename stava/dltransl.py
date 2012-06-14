# -*- coding: utf_8 -*-
from replacemap import replsX
from itertools import product
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

# TODO ta med '' i tabellerna, lägg till n '' i ett n långt ord i cc
""" calculates the distance """
def edit_dist(s1, s2,rules=replsX):
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
            d[(i,j)] = replaceX(s1,i,s2,j,d,rules)
                       #min(replaceX(s1,i,s2,j,d,rules)
                       #   ,insertX(s1,i,s2,j,d) # den här borde inte behövas :D
                       #   )
            
    res = d[lenstr1-1,lenstr2-1]
    return res

""" replacements """
def replaceX(s1,i,s2,j,d,rules):
  def replace1(s1,s2,i,j):
    ok = getRepl(rules,s1,s2)
    i0,j0 = i-1,j-1
    p = 3
    if ok!=None :
      mi,mj,p = ok
      i0 = i-mi
      j0 = j-mj
    return (i0,j0,p)
    
  same = issame(s1[i],s2[j])
  endi = i+1
  endj = j+1
  i0 = i-1
  j0 = j-1
  (i0,j0,p) = replace1(s1[:endi],s2[:endj],i,j)
  #(n0,m0,q) = replace1(s2[:endj],s1[:endi],j,i)
  return min(d[(i0,j0)]+p
  #          ,d[(m0,n0)]+q 
            ,d[i-1,j-1]+same)


def issame(a,b):
  if a==b:
    return 0
  if a in vow and b not in vow:
    return 3
  return 1
  
dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

        

def getRepl(rep,s1,s2):
  ret = (9,9,9) 
  for (a,b) in product([s1[-3:],s1[-2:],s1[-1:]],[s2[-3:],s2[-2:],s2[-1:]]):
    val = rep.get((a,b),None) 
    if val and val[2]<ret[2]:
      ret = val
  if ret!=(9,9,9):
    return ret



################################################################################
#NOT USED
################################################################################

#normal insert and delete
def insertX(s1,i,s2,j,d):
  (i0,j0,p) = insert1(s1,i,s2,j)
  (n0,m0,q) = insert1(s2,j,s1,i)
  best = min(d[(i0,j0)]+p 
            ,d[(m0,n0)]+q)
  return best

def insert1(s1,i,s2,j):
  val = 20
  if i<0:
    return (i-1,j-1,val)
  a = s1[i-1]
  b = s1[i]
  if a==b and a in dub:
    val -=4; 
  if a=='c' and b=='k':
     val -= 1
  return (i-1,j,float(val)/20)
 #
#
#  s1endswith = s1.endswith
#  s2endswith = s2.endswith
#  for ((a,b),val) in rep.iteritems():
#    if s1endswith(a) and s2endswith(b):
#      if val[2]<ret[2]:
#        ret = val # if val[2]<ret[2] else ret #min(val,ret,key=lambda (a,b,c): c)
#    #if ischange(s1,a) and b=='':
#    # v = val[2]
#    # return (1,0,v)
#  if ret!=(9,9,9):
#    return ret

def ischange(s,a):
  return (s.endswith(a))


