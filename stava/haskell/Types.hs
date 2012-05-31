module Types where
import Data.Map as M
import Data.ByteString
import Data.Set


type Iso = Integer
type Lemgram = ByteString
type Alpha = [Iso]
type Lex = M.Map Iso (Set (ByteString,Lemgram))
