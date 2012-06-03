module Types where
import Data.Map as M
import Data.ByteString
import Data.Set


type Iso = Integer
type Lemgram = ByteString
type Alpha = [Iso]
type Lex = M.Map Iso (Set (ByteString,Lemgram))
data WordStatus = InLex Lemgram | Variation VList | NotFound
  deriving Show
data Version = Old | New
type VList = [(ByteString,Lemgram,Double)]
