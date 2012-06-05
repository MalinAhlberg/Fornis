# -*- coding: utf_8 -*-
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

""" calculates the distance """
def edit_dist(s1, s2):
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
            d[(i,j)] = min(replaceX(s1,i,s2,j,d)
                          ,insertX(s1,i,s2,j,d)
                          )
            
    res = d[lenstr1-1,lenstr2-1]
    return res

""" replacements"""
def replaceX(s1,i,s2,j,d):
  val,same = 30,30
  endi = i+1
  endj = j+1
  i0 = i-1
  j0 = j-1
  if s1[i]==s2[j]:
    same = 0
  (i0,j0,p) = replace1(s1[:endi],s2[:endj],i,j)
  (n0,m0,q) = replace1(s2[:endj],s1[:endi],j,i)
  return min(d[(i0,j0)]+float(val-p)/30
            ,d[(m0,n0)]+float(val-q)/30 
            ,d[i-1,j-1]+same)

def replace1(s1,s2,i,j):
  ok = getRepl(replsX,s1,s2)
  i0,j0 = i-1,j-1
  p = 0
  if ok!=None :
    mi,mj,p = ok
    i0 = i-mi
    j0 = j-mj
  return (i0,j0,p*3)
   
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
 
dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

replsX = {(u'v',u'u'):(1,1,9) ,(u'v',u'w'):(1,1,9) ,(u'i',u'y'):(1,1,9) ,(u'i',u'j'):(1,1,9) ,(u'k',u'q'):(1,1,9)
         ,(u'k',u'c'):(1,1,9) ,(u'i',u'e'):(1,1,9) ,(u'u',u'o'):(1,1,9) ,(u'y',u'ö'):(1,1,9) ,(u'y',u'ö'):(1,1,9)
         ,(u'þ',u't'):(1,1,9), (u'ks',u'x'):(2,1,9),(u'gs',u'x'):(2,1,9),(u'ts',u'z'):(2,1,9),(u'ds',u'z'):(2,1,9)
         ,(u'aa',u'a'):(2,1,9),(u'r$',u'$'):(2,1,9),(u'th',u'þ'):(2,1,9),(u'gh',u'k'):(2,1,9),(u'dh',u't'):(2,1,9)
         ,(u'th',u't'):(2,1,9),(u'dh',u'd'):(2,1,9) ,(u'gh',u'g'):(2,1,9),(u'e$',u'a$'):(2,2,9),(u'^v',u'^hv'):(2,3,9)
         ,('w','u'):(1,1,9)
         # här börjar de nya
         ,(u'e',u'a'):(1,1,3)  ,(u'i',u'e'):(1,1,3) ,(u'n',u'm'):(1,1,3) ,(u'e',u'ä'):(1,1,3) ,(u'ö',u'o'):(1,1,3) 
         ,(u's',u'c'):(1,1,3) ,(u'j',u'g'):(1,1,3) ,(u'w',u'v'):(1,1,2) ,(u'c',u'k'):(1,1,2) ,(u's',u'z'):(1,1,3)
         ,(u'f',u'ff'):(1,2,3) ,(u'l',u'll'):(1,2,3) ,(u'ch',u'k'):(2,1,3) ,(u'e',u'a'):(1,1,3) ,(u'ee',u'e'):(2,1,3)
         ,(u'ij',u'i'):(2,1,3) ,(u'l',u'll'):(1,2,3) ,(u'ch',u'k'):(2,1,3) ,(u'e',u'a'):(1,1,3) ,(u'ee',u'e'):(1,1,3)}
         

def getRepl(rep,s1,s2):
  ret = (0,0,0) 
  for ((a,b),val) in rep.items():
    if s1.endswith(a) and s2.endswith(b):
      ret = max(val,ret,key=lambda (a,b,c): c)
  if ret!=(0,0,0):
    return ret


