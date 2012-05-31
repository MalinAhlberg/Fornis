module ReadXml where
import Text.XML.Light
import Text.XML.Light.Input
import Text.XML.Light.Types
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BSC
import qualified Data.Map as M
import qualified Data.Set as S
import Normalize
import Types
import Data.Maybe
import Control.Monad

--readText :: FilePath -> IO String
--readText fil = do
--  txt <- readFile fil
--  let xml  = onlyElems $ parseXML txt
--      Just body = msum $ map (findElement (unqual "body")) xml
--      txt  = iterText body
--  return "hej"
-- where iterText :: Element -> String
--       iterText e =  
--         strContent (findChildren e)
--  --return $ concatMap strContent body 

-- don't map over files, too much memory
readLex :: [FilePath] -> IO Lex
readLex files = readAccums files M.empty
  --maps <- readAccums files M.empty
  --return $ foldr (M.unionWith (++)) M.empty maps
 where readAccums :: [FilePath] -> Lex -> IO Lex
       readAccums [] lex = return lex
       readAccums (f:fs) lex = readAccum f lex >>= readAccums fs
       readAccum :: FilePath -> Lex -> IO Lex
       readAccum file lex = do
         txt <- readFile file
         let xml     = onlyElems $ parseXML txt
             entries = concatMap (findElements (unqual "LexicalEntry")) xml
         return $ insertK lex entries

       insertK lex []     = lex
       insertK lex (e:es) = 
          let Just (k,v) = mkDict e
          in  M.insertWith S.union k v $ insertK lex es
                                   --OBS fromJust

--             entries = concatMap (findElements (unqual "LexicalEntry")) xml
--             M.insertWith (++) $ catMaybes $ map mkDict entries

      -- readOne :: FilePath -> IO Lex
      -- readOne file = do
      --   txt <- readFile file
      --   let xml     = onlyElems $ parseXML txt
      --       entries = concatMap (findElements (unqual "LexicalEntry")) xml
      --       lex     = M.fromListWith (++) $ catMaybes $ map mkDict entries
      --   return lex

mkDict :: Element -> Maybe (Iso,S.Set (BS.ByteString,Lemgram))
mkDict entry = do
  lemgram <- getLemgram entry
  written <- getWrittenForm entry
  return (hashiso written,S.singleton (written,lemgram))

getLemgram :: Element -> Maybe Lemgram
getLemgram = getFeatVal "lemgram" return
   -- if old:
   --   lemma  = lemma.find('FormRepresentation')

getWrittenForm :: Element -> Maybe BS.ByteString
getWrittenForm = getFeatVal "writtenForm" 
                 (findElement (unqual "FormRepresentation"))

getFeatVal :: String -> (Element -> Maybe Element) -> Element -> Maybe BS.ByteString
getFeatVal qname contained entry = do
  lemma     <- findElement (unqual "Lemma") entry
  container <- contained lemma
  let feats = filterElementsName (== unqual "feat") container
  msum [fmap BSC.pack (findAttr (unqual "val") feat)
                          | feat <- feats
                          , let att = findAttr (unqual "att") feat
                          , att==Just qname]

 
      
