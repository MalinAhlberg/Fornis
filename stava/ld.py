# -*- coding: utf_8 -*-
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2)
"""
def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1,lenstr1+1):
        d[(i,-1)] = (i+1)#*10
    for j in xrange(-1,lenstr2+1):
        d[(-1,j)] = (j+1)#*10
 
    print d
    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = replace(s1[i],s2[j])
            print s1[i],s2[j]
            d[(i,j)] = min(
                           #d[(i-1,j)]   + delete(i,s1[i-1],s2[j]), # deletion
                           d[(i-1,j)]   + insert(i,s2[j],s1[i-1]), # deletion
                           d[(i,j-1)]   + insert(j,s2[j],s2[j+1]), # insertion
                           d[(i-1,j-1)] + cost,                    # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
        print d[(i,j)]
 
    print d
    return d[lenstr1-1,lenstr2-1]


dub = u"bdfgjlmnprstv"; #/* dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; #/* vokaler*/

# insert a before b
def insert(i,a,b):
  print 'insert',i,a,b
# change the first letter of a word
  val = 17
  if i==0:
    return val
  if a==b and a in dub:
    val -=4; 
  if a=='c' and b=='k':
    val -=1;
  print val
  return val


def replace(a,b):
  print 'replace',a,b
  val = 20
  if a in vow and b in vow:
    val -=1;
  ok = repls.get((a,b)) 
  if ok!=None:
    val -=ok
  print val
  return val
 
#define PARTCOST 25 /* kostnad per sammansättningsled */

#delete a before b
#def delete(i,a,b):
#  print 'delete',a,b
## change the first letter of a word
#  if i==0:
#    return 10
#  val = 20
#  if a==b and a in dub:
#    val -=4 
#  print val
#  return val

# other replace values
repls = {('e','a'):4 ,('a','e'):4 ,('e','i'):4 ,('i','e'):4 ,('n','m'):4
        ,('m','n'):4 ,('ä','e'):4 ,('e','ä'):4 ,('ö','o'):4 ,('o','ö'):4
        ,('s','c'):4 ,('g','j'):4 ,('j','g'):4 ,('v','w'):2 ,('w','v'):2
        ,('c','k'):2 ,('s','z'):4 ,('z','s'):4}

# ska vi bry oss om upper/lower case?
# ljudklasser
# sammansättningar


 
