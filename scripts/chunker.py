# -*- coding: utf_8 -*-
import re
from usefuls import *
#leta upp [,.¶]+Cap
#om Cap-ordet är romerska siffror, avbryt
#om förra ordet är förkortning, avbryt
#annars sätt [,.¶] STOP Cap
# stopmärke ska vara tag, använd subelement, .text och loopa över listan av ss
# . får använda toolkit
# paragraph behöver nog inget
# gör det här efter concattags, före pagenumber fix
# lägg till så att pagenumbers inte stör



def groupbyreg(txt,reg,mode): 
      chunks = []
      nxtchunk  = '' 
      while True:
        m = re.search(reg,txt,flags=re.UNICODE)
        if m:
           (st,end)    = m.span()
           (first,sec) = extractStartAndStop(m.group(),mode)
           chunk       = nxtchunk+txt[:st]+first
           chunks      += [chunk]
           nxtchunk    = sec
           txt         = txt[end:]
        else: 
           chunks += [nxtchunk+txt]
           break
      return chunks 

def extractStartAndStop(s,x):
    if x==1:
       return ('',s)
    if x==2:
       return (s[0],s[1:])


# upper case letters
uppers = "[ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖÞÆ]"

# TODO START here, get this expression to work together
p1 = '[\s>]#\s*[0-9]+'
p2 = '\[\s*‡‡\s*[0-9]+[abrv]*\s*\]'
p3 = '‡‡\s*[0-9]+[abrv]*'
pagenumbers = p1+'|'+p2+'|'+p3 #'(([\s>]#\s*[0-9]+)|(\[\s*‡‡\s*[0-9]+[abrv]*\s*\])|(‡‡\s*[0-9]+[abrv]*))*'


cpC = "[.,¶]\s*"+pagenumbers+'\s*'+uppers
