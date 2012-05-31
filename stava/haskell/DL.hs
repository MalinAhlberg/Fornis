module DL where
import Data.Array


editDistance :: Eq a => [a] -> [a] -> Int
editDistance xs ys = table ! (m,n)
    where
    (m,n) = (length xs, length ys)
    x     = array (1,m) (zip [1..] xs)
    y     = array (1,n) (zip [1..] ys)
 
    table :: Array (Int,Int) Int
    table = array bnds [(ij, dist ij) | ij <- range bnds]
    bnds  = ((0,0),(m,n))
 
    dist (0,j) = j
    dist (i,0) = i
    dist (i,j) = minimum [table ! (i-1,j) + 1, table ! (i,j-1) + 1,
        if x ! i == y ! j then table ! (i-1,j-1) else 1 + table ! (i-1,j-1)]

{-
"""
Compute the Damerau-Levenshtein distance between two given
strings (s1 and s2) but by considering special rules for how
expensive insertion and deletion is, depending on the letters
"""

edit_distdebug s1 s2 =
    let str1 = "^"++s1++"$"
        str2 = "^"++s2++"$"
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
            d[(i,j)] = min(replaceX(s1,i,s2,j,d)
                          ,insertX(s1,i,s2,j,d)
                          ,key=lambda(x,y):x
                          )
            
    res = d[lenstr1-1,lenstr2-1]
   -- for r in res[1]:
   --   print r
    return res[0]

-- calculates the distance
editDistance :: Eq a => [a] -> [a] -> Int
editDistance xs ys = table ! (m,n)
    where
    (m,n) = (length xs, length ys)
    x     = array (1,m) (zip [1..] xs)
    y     = array (1,n) (zip [1..] ys)
 
    table :: Array (Int,Int) Int
    table = array bnds [(ij, dist ij) | ij <- range bnds]
    bnds  = ((0,0),(m,n))
 
    dist (0,j) = j
    dist (i,0) = i
    dist (i,j) = minimum [replaceX s1 i s2 j table, insertX s1 i s2 j d]
    
replaceX s1 i s2 j d =

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
-- , d[(i0,j0)][1]+[Replace(s1[i0+1:endi],s2[j0+1:endj],float(val-p)/30)])
-- , d[(i0,j0)][1]+[Replace(s2[n0+1:endj],s1[m0+1:endi],float(val-q)/30)])
--   d[(i0,j0)][1]+[Replace(s1[i],s2[j],same)]))

def replace1(s1,s2,i,j):
  ok = getRepl(replsX,s1,s2)
  i0,j0 = i-1,j-1
  p = 0
  if ok!=None :
    mi,mj,p = ok
    i0 = i-mi
    j0 = j-mj
  return (i0,j0,p*3)
   
--normal insert and delete
def insertX(s1,i,s2,j,d):
  (i0,j0,p) = insert1(s1,i,s2,j)
  (n0,m0,q) = insert1(s2,j,s1,i)
  best = min(d[(i0,j0)]+p 
            ,d[(m0,n0)]+q)
  return best
-- , d[(i0,j0)][1]+[Del(s1[i0+1:i+1])])
--  , d[(m0,n0)][1]+[Del(s2[n0+1:j+1])]))
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
 
def replace(a,b):
  val = 10
  if a==b:
    return 0
  ok = repls.get((a,b)) or repls.get((b,a))
  if ok!=None :
    val -=ok
  elif a in vow and b in vow:
    val -=2;
  return float(val)/10

dub = u"bdfgjlmnprstv"; -- dubbeltecknande konsonanter */
vow = u"aeiouyåäöAEIOUYÅÄÖ"; -- vokaler*/

replaceMap = M.fromList replsX
replsX = [(x,(1,1,9)) | x <- [("v","u"),("v","w"),("i","y"),("i","j"),("k","q")
                           ,("k","c"),("i","e"),("u","o"),("y","ö"),("y","ö")
                           ,("þ","t"),("w","u")]]
         ++
         [(x,(2,1,9)) | x <- [("ks","x"),("gs","x"),("ts","z"),("ds","z")
                           ,("aa","a"),("r$","$"),("th","þ"),("gh","k")
                           ,("dh","t"),("th","t"),("dh","d"),("gh","g")]]
         ++
         [(("e$","a$"),(2,2,9)),(("^v","^hv"),(2,3,9))]
         -- här börjar de nya
         ++
         [(x,(1,1,3)) | x <- [("e","a"),("i","e"),("n","m"),("e","ä"),("ö","o") 
                             ,("s","c") ,("j","g") ,("s","z")]

def getRepl(rep,s1,s2):
  ret = (0,0,0) 
  for ((a,b),val) in rep.items():
    if s1.endswith(a) and s2.endswith(b):
      ret = max(val,ret,key=lambda (a,b,c): c)
  if ret!=(0,0,0):
    return ret

 
--normal insert and delete
def insert(s,i):
  val = 20
  if i<1 or i>len(s)-1:
     return val
  a = s[i-1]
  b = s[i]
  if a==b and a in dub:
    val -=4; 
  if a=="c" and b=="k":
     val -= 1
  return float(val)/20
-} 
