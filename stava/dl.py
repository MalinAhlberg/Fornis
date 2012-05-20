# -*- coding: utf_8 -*-
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

#TODO add more rules, calculate costs

# For debugging
class Del:
    def __init__(self,c):
        self.c = c

    def __str__(self):
        return "Del " + self.c.encode('utf8')

class Ins:
    def __init__(self,c):
         self.c = c

    def __str__(self):
        return "Ins " + self.c.encode('utf8')

class Replace:
    def __init__(self,fr,to):
         self.fr = fr
         self.to = to

    def __str__(self):
        if self.fr == self.to:
            return "Keep " + self.fr.encode('utf8')
        else:
            return "Replace " + self.fr.encode('utf8') + " with " + self.to.encode('utf8')

class Transpose:
    def __init__(self,a,b):
         self.a = a
         self.b = b

    def __str__(self):
        return u"Transpose " + self.a + " and " + self.b

# calculates the distance
def edit_dist(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    d[(-1,-1)] = (0,[])
    for i in xrange(0,lenstr1):
        d[(i,-1)] = (i+1,d[(i-1,-1)][1] + [Del(s1[i])])
    for j in xrange(0,lenstr2):
        d[(-1,j)] = (j+1,d[(-1,j-1)][1] + [Del(s2[j])])
 
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min((d[(i-1,j)][0] + insert(s1,i+1)        ,d[(i-1,j)][1] + [Del(s1[i])])
                          ,(d[(i,j-1)][0] + insert(s2,j+1)        ,d[(i,j-1)][1] + [Ins(s2[j])])
                          ,(d[(i-1,j-1)][0] + replace(s1[i],s2[j]),d[(i-1,j-1)][1] + [Replace(s1[i],s2[j])])
                          ,key=lambda(x,y):x
                          )
            if i>1 and j>1 and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)]
                               ,(d[(i-2,j-2)][0] + cost,d[(i-2,j-2)][1] + [Transpose(s1[i-1],s1[i])])
                               ,key=lambda(x,y):x) 
 
    res = d[lenstr1-1,lenstr2-1]
    for r in res[1]:
        print r
    return res[0]

def insert(s,i):
  val = 17
  if i<1 or i>len(s)-1:
     return val
  a = s[i-1]
  b = s[i]
  if a==b and a in dub:
    val -=4; 
  if a=='c' and b=='k':
     val -= 1
  return float(val)/17

def replace(a,b):
  if a==b:
    return 0
  val = 20
  if a in vow and b in vow:
    val -=1;
  ok = repls.get((a,b)) 
  if ok!=None:
    val -=ok
  return float(val)/20
 
dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

repls = {('e','a'):4 ,('a','e'):4 ,('e','i'):4 ,('i','e'):4 ,('n','m'):4
        ,('m','n'):4 ,(u'ä',u'e'):4 ,(u'e',u'ä'):4 ,('ö','o'):4 ,('o','ö'):4
        ,('s','c'):4 ,('g','j'):4 ,('j','g'):4 ,('v','w'):2 ,('w','v'):2
        ,('c','k'):2 ,('s','z'):4 ,('z','s'):4}

