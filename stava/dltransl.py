# -*- coding: utf_8 -*-
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

# For debugging
class Replace2:
    def __init__(self,s1,i,s2,j):
        if i<1 or i>len(s1)-1 or j<0 or j>len(s2)-1:
          self.a = 'dummy'
          self.b = 'dummy'
          self.x = 'dummy'
        else:
          self.a = s1[i-1] 
          self.b = s1[i]
          self.x = s2[j]

    def __str__(self):
        return "Replace two " + self.a.encode('utf8')+ self.b.encode('utf8')+' with '+ self.x.encode('utf8')

class CReplace:
    def __init__(self,s1,i,x):
        if i<1 or i>len(s1)-1:
          self.a = 'dummy'
          self.b = 'dummy'
          self.x = 'dummy'
        else:
          self.a = s1[i-1] 
          self.b = s1[i]
          self.x = x

    def __str__(self):
        return "Continue replace " + self.a.encode('utf8')+ self.b.encode('utf8')+' with '+ self.x.encode('utf8')


class Del:
    def __init__(self,c):
         self.c = c

    def __str__(self):
        return "Del " + self.c.encode('utf8')

class Replace:
    def __init__(self,fr,to):
         self.fr = fr
         self.to = to

    def __str__(self):
        if self.fr == self.to:
            return "Keep " + self.fr.encode('utf8')
        else:
            return "Replace " + self.fr.encode('utf8') + " with " + self.to.encode('utf8')

# calculates the distance
def edit_distdebug(s1, s2):
    s1 = '^'+s1+'$'
    s2 = '^'+s2+'$'
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    d[(-2,-2)] = (0,[])
    d[(-1,-2)] = (1,[])
    d[(-2,-1)] = (1,[])
    d[(-1,-1)] = (0,[])
    for i in xrange(0,lenstr1):
        d[(i,-1)] = (i+1,d[(i-1,-1)][1] + [Del(s1[i])])
        d[(i,-2)] = (i+2,d[(i-1,-1)][1] + [Del(s1[i])])
    for j in xrange(0,lenstr2):
        d[(-1,j)] = (j+1,d[(-1,j-1)][1] + [Del(s2[j])])
        d[(-2,j)] = (j+2,d[(-1,j-1)][1] + [Del(s2[j])])
 
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            d[(i,j)] = min((d[(i-2,j-1)][0] + replace2(s1,i,s2,j) ,d[(i-2,j-1)][1] + [Replace2(s1,i,s2,j)])
                          ,(d[(i-1,j-2)][0] + replace2(s2,j,s1,i) ,d[(i-1,j-2)][1] + [Replace2(s2,j,s1,i)])
                          ,(d[(i-1,j-1)][0] + replace(s1[i],s2[j])  ,d[(i-1,j-1)][1] + [Replace(s1[i],s2[j])])
                          # for normal variation
                          ,(d[(i-1,j)][0] + insert(s1,i+1)        ,d[(i-1,j)][1] + [Del(s1[i])])
                          ,(d[(i,j-1)][0] + insert(s2,j+1)        ,d[(i,j-1)][1] + [Del(s2[j])])
                          ,key=lambda(x,y):x

                          )
    res = d[lenstr1-1,lenstr2-1]
    for r in res[1]:
        if debug: print r
    return res[0]

def edit_dist(s1, s2):
    s1 = '^'+s1+'$'
    s2 = '^'+s2+'$'
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    d[(-2,-2)] = 0
    d[(-1,-2)] = 1
    d[(-2,-1)] = 1
    d[(-1,-1)] = 0
    for i in xrange(0,lenstr1):
        d[(i,-1)] = i+1
        d[(i,-2)] = i+2
    for j in xrange(0,lenstr2):
        d[(-1,j)] = j+1
        d[(-2,j)] = j+2
 
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            d[(i,j)] = min(d[(i-2,j-1)] + replace2(s1,i,s2,j)
                          ,d[(i-1,j-2)] + replace2(s2,j,s1,i)
                          ,d[(i-1,j-1)] + replace(s1[i],s2[j])
                          # for normal variation
                          ,d[(i-1,j)] + insert(s1,i+1)      
                          ,d[(i,j-1)] + insert(s2,j+1)       
                         # ,key=lambda(x,y):x

                          )
    res = d[lenstr1-1,lenstr2-1]
    return res



# TODO
#^hv     ^v
#a$ e$
def replace2(s1,i,s2,j):
  val = 30
  if i<1 or i>len(s1)-1 or j<0 or j>len(s2)-1:
    return 50
  a = s1[i-1]
  b = s1[i]
  x = s2[j]
  ok = repls.get((a+b,x))
  if ok!=None :
    val -= (ok*3)
  return float(val)/10
 
def replace(a,b):
  val = 10
  if a==b:
    return 0
  ok = repls.get((a,b)) or repls.get((b,a))
  if ok!=None :
    val -=ok
#  elif a in vow and b in vow:
#    val -=2;
  return float(val)/10


dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

repls = {('v','u'):9 ,('v','w'):9 ,('i','y'):9 ,('i','j'):9 ,('k','q'):9
        ,('k','c'):9 ,('i','e'):9 ,('u','o'):9 ,(u'y',u'ö'):9 ,(u'y',u'ö'):9
        ,('þ','t'):9, ('ks','x'):9,('gs','x'):9,('ts','z'):9,('ds','z'):9,('aa','a'):9
        ,('r$','$'):9,('th','þ'):9,('gh','k'):9,('dh','t'):9,('th','t'):9,('dh','d'):9
        ,('gh','g'):9,('e$','a$'):9,('^v','hv'):9,('w','u'):9
        # här börjar de nya
        ,('e','a'):3  ,('i','e'):3 ,('n','m'):3 ,(u'e',u'ä'):3 ,('ö','o'):3 
        ,('s','c'):3 ,('j','g'):3 ,('w','v'):2 ,('c','k'):2 ,('s','z'):3}

 
#normal insert and delete
def insert(s,i):
  val = 20
  if i<1 or i>len(s)-1:
     return val
  a = s[i-1]
  b = s[i]
  if a==b and a in dub:
    val -=4; 
  if a=='c' and b=='k':
     val -= 1
  return float(val)/20
 
