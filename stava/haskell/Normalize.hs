module Normalize where
import qualified Data.Map as M
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BSC
import Data.Char hiding (isLetter)
import Data.Set hiding (map,filter)
import Types


normalize :: [BS.ByteString] -> M.Map Iso (Set BS.ByteString)
normalize = 
  M.fromListWith union . map (\w -> let normw = norm w in (hashiso normw,singleton normw)) 

iso :: Char -> Iso
iso c = (toEnum $ if isLetter c then ord (toLower c) else 0) ^ 5

hashiso :: BS.ByteString -> Iso
hashiso = sum . map iso . BSC.unpack
  
norm :: BS.ByteString -> BS.ByteString
norm = BSC.pack . map toLower . filter isLetter . BSC.unpack

(|||) :: (a -> Bool) -> (a -> Bool) -> a -> Bool
f ||| g = \x -> f x || g x

isLetter = isAlpha ||| (`elem` "^$")

--normalisera:
--  gå igenom allt
--  sätt alfabet (alla små bokstäver) key(w) = sum [(iso c)^n | c <- w] (n = 5)
--  normalisera...
--  bygg frekvenslista, räkna bort punkter osv


