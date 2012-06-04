{-# LANGUAGE TupleSections #-}
module DL where
import Data.Array
import Data.Word
import Data.Maybe
import Data.List hiding (insert)
import Debug.Trace
import qualified Data.ByteString as B
import qualified Data.Map as M
import qualified Data.ByteString.Char8 as BC

ed a b = editDistance (BC.pack a) (BC.pack b)

--TODO use Array instead of String? ByteString?
--editDistance :: a -> a -> (a -> Int -> Char) -> Double
editDistance :: B.ByteString -> B.ByteString -> Double
editDistance xs ys = table ! (m,n)
    where
    str1 = w8 '^'+++xs+++w8 '$'
    str2 = w8 '^'+++ys+++w8 '$'
    (m,n) = (B.length str1-1, B.length str2-1)
--    x     = array (1,m) (zip [1..] xs)
--    y     = array (1,n) (zip [1..] ys)
 
    table :: Array (Int,Int) Double
    table = array bnds [(ij, dist ij) | ij <- range bnds]
    bnds  = ((-1,-1),(m,n))
 
    dist (-1,j) = toEnum j+1
    dist (i,-1) = toEnum i+1
    dist (i,j) = let opts = map ($ (str1,i,str2,j,table)) [replace,insert]
                 in  minimum opts

--minimum = minimumBy (compare `on` thrd)
--  where thr (a,b,c) = c
(+++) :: B.ByteString -> B.ByteString -> B.ByteString                              
a +++ b = a `B.append` b

w8 :: Char -> B.ByteString
w8 = BC.singleton
   
--normal insert and delete
insert :: (B.ByteString,Int,B.ByteString,Int,Array (Int,Int) Double) -> Double
insert (s1,i,s2,j,d) =
  let (i0,j0,p) = insert1 s1 i j 
      (n0,m0,q) = insert1 s2 j i 
  in minimum[d ! (i0,j0) +p, d ! (m0,n0) +q]
 where 
  val=20
  insert1 s1 i j | i<1                    = (i-1,j-1,val) -- nothing to insert
  insert1 s1 i j | a==b && a `elem` dub   = (i-1,j,(val-4)/val)
                 | a== 'c' && b== 'k'     = (i-1,j,(val-1)/val)
                 | otherwise              = (i-1,j,val/val)
   where a = s1 `BC.index` (i-1)
         b = s1 `BC.index` i
   
replace :: (B.ByteString,Int,B.ByteString,Int,Array (Int,Int) Double) -> Double
replace (s1,i,s2,j,d) =
  let (i0,j0,p) = replace1 s1 i s2 j 
      (n0,m0,q) = replace1 s2 j s1 i 
  in minimum[d ! (i0,j0) +p, d ! (m0,n0) +q,d ! (i-1,j-1) +same]
 where a    = s1 `BC.index` i   
       b    = s2 `BC.index` j
       val  = 30
       same = if a==b then 0 else 10
       replace1 s1 i s2 j = 
         --case getReplace (drop (i-1) $ take (1+i) s1) (drop (j-1) $ take (1+j) s2) of
         case getReplace s1 i s2 j of
              Nothing      -> (i-1,j-1, val/val)
              Just (a,b,c) -> (i-a,j-b,(val-toEnum c*3)/val)

getReplace :: B.ByteString -> Int -> B.ByteString -> Int -> Maybe (Int,Int,Int)
getReplace s1 i s2 j = maximum $ Nothing:res
  
 where a    = w8 $ s1 `BC.index` i   
       b    = w8 $ s2 `BC.index` j
       aa   = B.drop (i-1) $ B.take (i+1) s1 --s1 `BC.index` i+1:[a]
       bbb  = B.drop (j-2) $ B.take (j+1) s2
       val  = 30
       res  = map Just $ concat $ catMaybes [findInMap a b replaceMap1, findInMap aa bbb replaceMap2]

-- b should be 3 chars (or few atleast)
findInMap :: B.ByteString -> B.ByteString -> M.Map B.ByteString [(B.ByteString,(Int,Int,Int))] -> Maybe [(Int,Int,Int)]
findInMap a b map = do
   x <- M.lookup a map
   return [v | (b',v) <- x, b' `B.isSuffixOf` b]


--getReplace :: B.ByteString -> Int -> B.ByteString -> Int -> Maybe (Int,Int,Int)
--getReplace s1 s2 = maximum $
--  Nothing:[Just v | ((a,b),v) <- replaceMap, a `isSuffixOf` s1 && b `isSuffixOf` s2]

dub = "bdfgjlmnprstv";      -- dubbeltecknande konsonanter 
vow = "aeiouyåäöAEIOUYÅÄÖ"; -- vokaler

-- 1 to 1 replacements
replaceMap1 :: M.Map B.ByteString [(B.ByteString ,(Int,Int,Int))]
replaceMap1 = M.fromList $
  [(BC.pack a,map (\b -> (BC.pack b,(1,1,9))) b)
      | (a,b) <- [("v",["u","w"]),("i",["y","j","e"]),("k",["q","c"])
                 ,("u",["o"]),("y",["ö"]) ,("þ",["t"])]]
   ++
   [(BC.pack a,map (\b -> (BC.pack b,(1,1,3))) b)
      | (a,b) <- [("e",["a","ä"]),("n",["m"]),("ö",["o"])
                 ,("s",["c","z"]) ,("j",["g"])]]


-- 2 to 1, 2 to 2, 2 to 3 replacements
replaceMap2 :: M.Map B.ByteString [(B.ByteString ,(Int,Int,Int))]
replaceMap2 = M.fromList $
  [(BC.pack a,map (\b -> (BC.pack b,(2,1,9))) b)
     | (a,b) <- [("ks",["x"]),("gs",["x"]),("ts",["z"]),("ds",["z"])
                      ,("aa",["a"]),("r$",["$"]),("th",["þ"]),("gh",["k"])
                      ,("dh",["t"]),("th",["t"]),("dh",["d"]),("gh",["g"])]]
   ++
   [(BC.pack "e$",[(BC.pack "a$",(2,2,9))]),(BC.pack "^v",[(BC.pack "^hv",(2,3,9))])]

--
--replaceMap :: [((B.ByteString,B.ByteString),(Int,Int,Int))]
--replaceMap = 
--  [((BC.pack a,BC.pack),(1,1,9)) | (a,b) <- [("v","u"),("v","w"),("i","y"),("i","j"),("k","q")
--                   ,("k","c"),("i","e"),("u","o"),("y","ö"),("y","ö")
--                   ,("þ","t"),("w","u")]]
--   ++
--   [(x,(2,1,9)) | x <- [("ks","x"),("gs","x"),("ts","z"),("ds","z")
--                      ,("aa","a"),("r$","$"),("th","þ"),("gh","k")
--                      ,("dh","t"),("th","t"),("dh","d"),("gh","g")]]
--   ++
--   [(("e$","a$"),(2,2,9)),(("^v","^hv"),(2,3,9))]
--   -- här börjar de nya
--   ++
--   [(x,(1,1,3)) | x <- [("e","a"),("i","e"),("n","m"),("e","ä"),("ö","o") 
--                       ,("s","c") ,("j","g") ,("s","z")]]
