module DL where
import Data.Array
import Data.List hiding (insert)
import Debug.Trace


--TODO use Array instead of String? ByteString?
--editDistance :: a -> a -> (a -> Int -> Char) -> Double
editDistance :: String -> String -> Double
editDistance xs ys = table ! (m,n)
    where
    str1 = '^':xs++"$"
    str2 = '^':ys++"$"
    (m,n) = (length str1-1, length str2-1)
    x     = array (1,m) (zip [1..] xs)
    y     = array (1,n) (zip [1..] ys)
 
    table :: Array (Int,Int) Double
    table = array bnds [(ij, dist ij) | ij <- range bnds]
    bnds  = ((-1,-1),(m,n))
 
    dist (-1,j) = toEnum j+1
    dist (i,-1) = toEnum i+1
    dist (i,j) = let opts = map ($ (str1,i,str2,j,table)) [replace,insert]
                 in  minimum opts

--minimum = minimumBy (compare `on` thrd)
--  where thr (a,b,c) = c
                              
   
--normal insert and delete
insert :: (String,Int,String,Int,Array (Int,Int) Double) -> Double
insert (s1,i,s2,j,d) =
  let (i0,j0,p) = insert1 s1 i j 
      (n0,m0,q) = insert1 s2 j i 
  in minimum[d ! (i0,j0) +p, d ! (m0,n0) +q]
 where 
  val=20
  insert1 s1 i j | i<1                  = (i-1,j-1,val) -- nothing to insert
  insert1 s1 i j | a==b && a `elem` dub = (i-1,j,(val-4)/val)
                 | a=='c' && b=='k'     = (i-1,j,(val-1)/val)
                 | otherwise            = (i-1,j,val/val)
   where a = s1 !! (i-1)
         b = s1 !! i
   
replace :: (String,Int,String,Int,Array (Int,Int) Double) -> Double
replace (s1,i,s2,j,d) =
  let (i0,j0,p) = replace1 s1 i s2 j 
      (n0,m0,q) = replace1 s2 j s1 i 
  in minimum[d ! (i0,j0) +p, d ! (m0,n0) +q,d ! (i-1,j-1) +same]
 where a    = s1 !! i   
       b    = s2 !! j
       val  = 30
       same = if a==b then 0 else 10
       replace1 s1 i s2 j = 
         case getReplace (drop (i-1) $ take (1+i) s1) (drop (j-1) $ take (1+j) s2) of
              Nothing      -> (i-1,j-1, val/val)
              Just (a,b,c) -> (i-a,j-b,(val-toEnum c*3)/val)

getReplace :: String -> String -> Maybe (Int,Int,Int)
getReplace s1 s2 = maximum $
  Nothing:[Just v | ((a,b),v) <- replaceMap, a `isSuffixOf` s1 && b `isSuffixOf` s2]

dub = "bdfgjlmnprstv";      -- dubbeltecknande konsonanter 
vow = "aeiouyåäöAEIOUYÅÄÖ"; -- vokaler

replaceMap :: [((String,String),(Int,Int,Int))]
replaceMap = 
  [(x,(1,1,9)) | x <- [("v","u"),("v","w"),("i","y"),("i","j"),("k","q")
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
                       ,("s","c") ,("j","g") ,("s","z")]]


