import qualified Data.Map as M
import Data.Maybe
import Normalize
--TAV: för ett ord, antistrip, kolla av, räkna ut av:t för varje bi- och ev. trigram.
--        spara. = alfabet
--få cc = variationer:
--             transpositions -automatiskt
--             deletions      - gå igenom alfabetet och kolla ordet plus varje aav(bokstavish)
--             insertions - gå ingenom tav:en och kolla ordet-minus varje tav
--             substitute - gå igenom både tav och aav och lägg till varje aav och ta bort ett tav
--

type Lemgram = String
--type Lex = M.Map Iso (String,Lemgram)
type Lex = M.Map Iso [(String,Lemgram)]
type Alpha = [Iso]

-- finds the 'aav' alphabet, consisting of all strings, bigram and trigrams
alphabet :: [String] -> [Iso]
alphabet wds = concat [tolist(gettav w) |  w <-  wds]

tolist :: ([a],[a],[a]) -> [a]
tolist (a,b,c) = a++b++c
   
-- gets the av:s for a string
gettavkeep w = gettav' w ("^"++w++"$")
gettav w     = gettav' w ("_"++w++"_")
gettav' :: String -> String -> ([Iso],[Iso],[Iso])
gettav' str ended = 
  let unis  = map iso str
      bis   = getns 2 ended
      tris  = if length str>5 then getns 3 ended else []
      getns n = map isos . takeWhile ((==n) . length) . map (take n) . iterate (drop 1)
      isos    = sum . map iso
  in  (unis,bis,tris)

-- gets character confusion, the set of words comparable to this one
-- how deep should we go? just one del/sub or insertion?
getccs :: (String,Iso) -> Lex -> Alpha -> [(String,Lemgram)]
getccs (w,av) lex alphabet =  
   let transpos = M.lookup av lex
       deletes  = map (+av) alphabet
       tav      = tolist $ gettav w
       subs     = concatMap (\aav -> map (av+aav+) tav) alphabet
       inserts  = map (av-) tav
   in concat $ catMaybes (transpos 
                          : (map (flip M.lookup lex) $ deletes++subs++inserts))


inLex :: Lex -> Iso -> Bool
inLex = undefined --isJust . flip M.lookup

   
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
