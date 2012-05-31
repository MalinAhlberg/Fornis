{-# LANGUAGE NamedFieldPuns #-}
module GetData where
import Extracttxt
import Normalize
import Types
import CC
import ReadXml
import Control.Monad
import Control.Arrow
import Data.Functor
import Data.Char
import Data.List
import Debug.Trace
import qualified Data.Map as M
import qualified Data.Set as S
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BSC

data Status = S {types, tokens, goodW, goodT, badW, badT, varW, varT :: Int}
emptyStatus = S {types = 0 ,tokens = 0, goodW = 0, goodT = 0
                ,badW = 0, badT = 0, varW = 0, varT = 0}
outputWords = "smalltestallmar"
outputData  = "smalltestdatamar"

sammanstall :: IO ()
sammanstall = do
  let files = ["../Test.xml"]
  hashd <- readLex oldlex --dalin,old=True) --oldlex
  putStrLn "have lex"
 -- alpha <-  getvariant('lex_variation.txt')
  res <- mapM (getData hashd) files
  writeFile outputData (shownice res)

oldlex = ["../../scripts/lexiconinfo/newer/schlyter.xml"
         ,"../../scripts/lexiconinfo/newer/soederwall_main.xml"
         ,"../../scripts/lexiconinfo/newer/soederwall_supp.xml"]
dalin =  ["../../../Lexicon/dalin.xml"]

getData :: Lex -> FilePath -> IO (FilePath,Status) --IO (M.Map String (Int,WordStatus))
getData hashd fil = do
  putStrLn fil
  txt <- words <$> readFile fil 
  putStrLn "have file"
  let wds      = map (norm . BSC.pack . map toLower) txt
      --alpha    = normalize wds, don't want to use??
      alpha    = alphabet wds
      textdic  = mkTextDic wds --do we need this?
      spelldic = mkSpellDic alpha textdic M.empty
      stats    = calculate spelldic
  -- spelldic is too hard to compute, even with minimal lexicon
  --print spelldic
  putStrLn "calculate..."
  printOutput wds spelldic
  return (fil,stats)

 where mkTextDic :: [BS.ByteString] -> [(BS.ByteString,Int)]
       mkTextDic = (map (head &&& length)) . group . sort
       createSpells :: Alpha -> (BS.ByteString,Int) -> (BS.ByteString,(Int,WordStatus))
       createSpells alpha (w,i) = (w,(i,spellcheckword w hashd alpha))
       mkSpellDic :: Alpha -> [(BS.ByteString,Int)] -> M.Map BS.ByteString (Int,WordStatus)  -> M.Map BS.ByteString (Int,WordStatus) 
       mkSpellDic _ [] lex = lex
       mkSpellDic alpha (x:xs) lex = 
          let (k,v) = createSpells alpha x
          in  M.insert k v $ mkSpellDic alpha xs lex
             --M.fromList $ map (createSpells alpha) textdic

--TODO where to calculate distance??
printOutput :: [BS.ByteString] -> M.Map BS.ByteString (Int,WordStatus) -> IO ()
printOutput wds spellmap = do
 appendFile outputWords ("\n\n\n"++ (unlines $ map out wds))
 where out :: BS.ByteString -> String
       out w = let strw = BSC.unpack w
               in case M.lookup w spellmap of
                    Just (i,InLex lemgram) -> intercalate "\t" [strw,"Found",BSC.unpack lemgram,show i]
                    Just (i,Variation xs)  -> intercalate "\t" [strw,"Variations",pretty xs,show i]
                    Just (i,NotFound)      -> intercalate "\t" [strw,"Not Found",show i]
                    _                      -> intercalate "\t" [strw,"Not Found",show 0]
       pretty :: S.Set (BS.ByteString,Lemgram,Int) -> String
       pretty xs = intercalate " - " (map pr $ S.toList xs)
       pr (s,l,i) = BSC.unpack s++" ("++show i++BSC.unpack l++") "

shownice :: [(FilePath,Status)] -> String
shownice = unlines . map printit
  where printit :: (FilePath,Status) -> String
        printit (f,s) = unwords
                          [f,"good",show (goodW s),"(",show (goodT s),"bad"
                          ,show (badW s),"(",show (badT s),"variantions"
                          ,show (varW s),"(",show (varT s),"***"]


--TODO count total!
calculate ::  M.Map BS.ByteString (Int,WordStatus) -> Status
calculate spelldic =
   let dict    = M.toList spelldic
       (res,_) = mapAccumL f emptyStatus dict 
  in res
 where f :: Status -> (BS.ByteString,(Int,WordStatus)) -> (Status,Char)
       f s (w,(i,st)) = case st of
         InLex     _ -> (s {goodW = goodW s + i,goodT = goodT s +1},' ')
         NotFound    -> (s {badW = badW s + i,badT = badT s +1},' ')
         Variation _ -> (s {varW = varW s + i,varT = goodT s +1},' ')

