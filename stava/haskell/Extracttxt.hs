module Extracttxt where
import ReadXml
import Normalize
import CC
import Types
import qualified Data.Map as M
import qualified Data.Set as S
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BSC

--TODO START the handeling of $^ vs _ gets different results. Which ones do we want?
-- read and collect all text in xml. but we only get more by being less strict
gettext :: FilePath -> IO String
gettext fil = undefined --read xml

lexicons = --["../scripts/kast.xml"]
           ["../scripts/lexiconinfo/newer/schlyter.xml"
           ,"../scripts/lexiconinfo/newer/soederwall_main.xml"
           ,"../scripts/lexiconinfo/newer/soederwall_supp.xml"]

data WordStatus = InLex Lemgram | Variation (S.Set (BS.ByteString,Lemgram,Int)) | NotFound
  deriving Show
data Version = Old | New

{-
  spellcheckword(word,hashlexicon,alphabet of ok variants,alphabet of hash-grams)
  returns (False,(word,lemgram)) if the word is in the lexicon
  returns (True,(word,variant,distance,lemgram)) if variants are found
  returns (False,None) if nothing interesting is found
-}
spellcheckword :: BS.ByteString -> Lex -> Alpha -> WordStatus
spellcheckword w lex alpha = 
  let av = hashiso w in
  case findWordInLex (w,av) lex of
       Just lem -> InLex lem
       Nothing  -> let set = getccs (w,av) lex alpha
                   in if S.null set then NotFound else Variation set
                    
findWordInLex :: (BS.ByteString,Iso) -> Lex -> Maybe Lemgram
findWordInLex (w,av) lex = 
  case M.lookup av lex of  
       Just xs -> lookup w $ S.toList xs
       Nothing -> Nothing


{-
def insert(d,form,lem):
    key = sum([iso(c) for c in form])
    old = d.get(key)
    if old!=None:
      old.update({form:lem})
    else:
      d.update({key : {form : lem}})

if __name__ == "__main__":
   lookup()

def supertest():
    txt    = ' '.join(list(gettext('../filerX/Luk41SLundversion.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    print len(set(wds))
 
def spellchecksmall(w,d,alpha):
  lem = getlemgram(d,w)
  if lem==None:
    ccs = [(w,getchanges(w,d,alpha))]
    res = getvariant(ccs)
    if res:
      return (True,res)
  else:
    return (False,(w,lem))
  return (False,None)
 
 
def getvariant(ccs):
  from math import fabs
  var = []
  for (w,cc) in ccs:
    for (c,lem) in set(cc):
      if fabs(len(w)-len(c))<=len(w)/2:
        dist = edit_dist(w,c)
        if dist<2:
          var.append((w,c,dist,lem))
          --return(True,(w,c,dist,lem))
  var.sort(key=lambda (w,c,dist,lem): dist)
  return var


def shownice(xs):
    slist = ['\t'.join([unicode(w) for w in x]) for x in xs]
    s = "\n".join(slist)
    return s


-- reads lexicons and a text and idenitfies spelling variations,
-- using the lexicons as a standard
--lookup :: [Variant] -> String -> Lex
lookup :: String -> IO a
lookup  =
                        --read variants
                        --read lexicons
    wds   <- words <$> gettext "../filerX/Albinus.xml"
    lex   <- readLex lexicons
    alpha <- getvariant "lex_variation.txt"
    let gramMap = normalize wds
    map (classify lex alpha gramMap) wds


    oks    = []
    inlex  = []
    print 'will find ccs and rank'
    -- TODO tråda här? blir ej snabbare!
    --queue = Queue.Queue(0)
    wds = set(wds)
    for w in wds:
    --  print w
    --  t = threading.Thread(target=spellcheckword,args=(w,d,alpha,a,oks,inlex,queue))
      --t.start()
      (ok,arg) = spellcheckword(w,d,alpha,a)
      if ok:
        oks.append(arg)
      elif arg!=None:
        inlex.append(arg)
        
    --for i in wds:
    --  a = queue.get()
    --  oks += a
    oks = sorted(set(oks),key= lambda (w,c,d,l): d)
    codecs.open('variant2','w',encoding='utf8').write(shownice(oks))
    codecs.open('inlex','w',encoding='utf8').write(shownice(inlex))


 -}
