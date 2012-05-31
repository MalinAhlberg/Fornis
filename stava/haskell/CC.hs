module CC where
import qualified Data.Map as M
import qualified Data.Set as S
import Data.Maybe
import Data.Char
import Data.List
import Control.Arrow hiding ((+++))
import Debug.Trace
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BSC
import Normalize
import Types
import DL
--TAV: för ett ord, antistrip, kolla av, räkna ut av:t för varje bi- och ev. trigram.
--        spara. = alfabet
--få cc = variationer:
--             transpositions -automatiskt
--             deletions      - gå igenom alfabetet och kolla ordet plus varje aav(bokstavish)
--             insertions - gå ingenom tav:en och kolla ordet-minus varje tav
--             substitute - gå igenom både tav och aav och lägg till varje aav och ta bort ett tav
--


test = do
  txt <- readFile "../Test.xml"
  let wds  = map (norm . BSC.pack . map toLower) $ words txt
  print $ length $ alphabet wds
--      alpha = alphabet wds
--      xs = sort $ map (length &&& head) $ group $ sort alpha
--  print $ length $ nub $ alphabet wds
--  print $ length $ dropWhile ((<50) . fst) xs

-- finds the 'aav' alphabet, consisting of all strings, bigram and trigrams
-- TODO remove the restriction on alphas when possible
alphabet :: [BS.ByteString] -> Alpha
alphabet wds = --nub $ concat [tolist(gettav w) |  w <-  wds]
               let  as = concat [tolist(gettav w) |  w <-  wds]
                    xs = sort $ map (length &&& head) $ group $ sort as
               in  map snd $ dropWhile ((<50) . fst) xs

tolist :: ([a],[a],[a]) -> [a]
tolist (a,b,c) = a++b++c
   
-- gets the av:s for a string
gettavkeep w = gettav' w (BSC.pack "^"+++w+++BSC.pack "$")
gettav w     = gettav' w (BSC.pack "_"+++w+++BSC.pack "_")
gettav' :: BS.ByteString -> BS.ByteString -> ([Iso],[Iso],[Iso])
gettav' str ended = 
  let len   = BS.length str
      unis  = map iso $ BSC.unpack str 
      bis   = if len>3 then getns 2 ended else []
      tris  = if len>5 then getns 3 ended else []
      getns n = map isos . takeWhile ((==n) . length) . map (take n) . iterate (drop 1) . BSC.unpack
      isos    = sum . map iso
  in  (unis,bis,tris)

-- gets character confusion, the set of words comparable to this one
-- how deep should we go? just one del/sub or insertion?
getccs :: (BS.ByteString,Iso) -> Lex -> Alpha -> S.Set (BS.ByteString,Lemgram,Int)
getccs (w,av) lex alphabet =  
   let transpos = M.lookup av lex
       deletes  = map (+av) alphabet
       tav      = tolist $ gettav w
       subs     = concatMap (\aav -> map (av+aav-) tav) alphabet
       inserts  = map (av-) tav
       all      = (S.toList $ S.fromList(deletes++subs++inserts))
     in S.fromList $ f w {-transpos OBS-} all lex []
--   in S.fromList $ filter (isOk w) $ concat $ catMaybes (transpos 
--                          : (map (flip M.lookup lex) $ S.toList $ S.fromList(deletes++subs++inserts)))

f :: BS.ByteString -> [Iso] -> Lex -> [(BS.ByteString,Lemgram,Int)] -> [(BS.ByteString,Lemgram,Int)]
f s [] lex set = set
f s (x:xs) lex set = let mwl  = M.lookup x lex 
                         res  = case mwl of
                                  Just wls -> [(v,l,d) | (v,l) <- S.toList wls --S.toList $ S.fromList wls --does not help
                                                       ,let (s',v') = (BSC.unpack v,BSC.unpack s)
                                                       ,let d = editDistance s' v'
                                                       --,abs (length s'-length v')<3 --does not help
                                                       ,d<3]
                                  Nothing  -> []
                         --maybe [] (map (editDistance (BSC.unpack s) . BSC.unpack . fst)) mwl
                         set' = f s xs lex set
                     in res ++ set'

--isOk :: BS.ByteString -> (BS.ByteString,Lemgram) -> Bool
--isOk w (v,l) = editDistance (BSC.unpack w) (BSC.unpack v) <3

(+++) :: BS.ByteString -> BS.ByteString -> BS.ByteString
(+++) = BS.append
{-

       
def getchanges(w,lex,changeset): -- lex = korpuslex of avs
    ccs = []                     -- changeset = {900:[2,1]},{2:[900]} = (hv,v)
    (u,b,t) = gettav(w,keep=True)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    -- substitutions only
    for tav in tavs:
      -- get diff between tav and its translations
      subs = changeset.get(tav) or []
      ch += map(lambda x: x-tav,subs)
    [addAll(lex.get(av+sum(c)),ccs) for c in powerset(set(ch)) if av+sum(c)>0]
    return ccs

def powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])

-------------- CAN BE REMOVED
def getchangestest(w): -- lex = korpuslex of avs
    import readvariant
    changeset  = readvariant.getvariant('lex_variation.txt')
    ccs = []                     -- changeset = {900:[2,1]},{2:[900]} = (hv,v)
    (u,b,t) = gettav(w)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    -- substitutions only
    for tav in tavs:
      if tav ==25937424601L: print 'found y'
      -- get diff between tav and its translations
      subs = changeset.get(tav) or []
      if  12762815625L in subs: print 'found i'
      ch += map(lambda x: x-tav,subs)
--    for c in powerset(set(ch)):
--      addAll(lex.get(av+sum(c)),ccs)
    return [av+sum(c) for c in powerset(set(ch)) if av+sum(c)>0]

-- TODO, give a value to the word pair depending on dl and how
-- often the other one appears, as well as word length
-- remove exact copies
def limit(w,ccset):
    props = []
    for (cc,n) in ccset:
      dist = dl.edit_dist(cc,w)
      if dist > lim:
        props.append((cc,n,dist))
        -- TODO more snajs rules here
    return props
-} 

