module Normalize where
import qualified Data.Map as M
import Data.Char hiding (isLetter)
import Data.Set hiding (map,filter)

type Iso = Integer

normalize :: [String] -> M.Map Iso (Set String)
normalize = 
  M.fromListWith union . map (\w -> let normw = norm w in (hashiso normw,singleton normw)) 

iso :: Char -> Iso
iso c = (toEnum $ if isLetter c then ord (toLower c) else 0) ^ 5

hashiso :: String -> Iso
hashiso = sum . map iso
  
norm :: String -> String
norm = filter isLetter 

(|||) :: (a -> Bool) -> (a -> Bool) -> a -> Bool
f ||| g = \x -> f x || g x

isLetter = isAlpha ||| (`elem` "^$")

--normalisera:
--  gå igenom allt
--  sätt alfabet (alla små bokstäver) key(w) = sum [(iso c)^n | c <- w] (n = 5)
--  normalisera...
--  bygg frekvenslista, räkna bort punkter osv


