# -*- coding: utf_8 -*-
import re
import os
from xml.etree import ElementTree as etree
from nltk.tokenize import PunktSentenceTokenizer
import cPickle as pickle

# Segments text into sentences. Puts each sentence in an <s> xml elemnt
# Uses four modes to decide how the segmentation should be done:
# 'cap'   splits a sentence whenever a word is capitalized
# 'cpC'   splits after punctuation, comma or '¶' (unicode symbol),
#           if the following word is capitalized
# 'punkt' splits at punctuation, uses nltk
# 'para'  uses predefined paragraphs, does not split further
# 'cap' and 'cpC' ignores page numberings and roman numbers.


# for makefile. put segmentF and chunker in the directory, as well as sentenceinfo
#custom_common = sentence
#%.sentence: %.TEXT %.$(sentence_chunk)
#	python -m segmentF --element s --out $@ --text $(1) --chunk $(2) --segmenter $(sentence_segmenter) --model
# 

sentence_dir = '../sentenceinfo'

def grouptext(txt,mode,segmenter=None):
    return groupbyreg(txt,regex(mode),mode,segmenter)

# reads files in sentence_dir and adds the correct encoding
def findmode(fil):
    fil,ext = os.path.splitext(os.path.basename(fil))
    print 'find file',fil
    def findFile(path):
      txt = open(path,'r').readlines()
      isInFile = False
      for line in txt:
          splitted = line.split()
          if splitted:
            (file2,ext2) = os.path.splitext(os.path.basename(splitted[0]))
            if file2 == fil:
             isInFile = True
      return isInFile

    if findFile(os.path.join(sentence_dir,'dot.txt')):
      return 'punkt'
    elif findFile(os.path.join(sentence_dir,'dotComma.txt')):
      return 'cpC'
    elif findFile(os.path.join(sentence_dir,'paras.txt')):
      return 'para'
    elif findFile(os.path.join(sentence_dir,'capital.txt')):
      return 'cap'
    else:
      return 'punkt'

def span_tokenize(text,mode,segmenter=None):
    """
    Given a text, returns a list of the (start, end) spans of sentences
    in the text.
    """
    #if segmenter is not None:
    #    lst = segmenter.span_tokenize(text)
    #else:
    slices = grouptext(text,mode,segmenter)
    i  = 1
    i0 = 0
    lst = []
    for sl in slices:
      if len(sl)!=0:
        j = i+len(sl)-1
        lst += [(i0,j)]
        i   = j+1
        i0  = i
    return lst


# returs appropiate regex for the modes
def regex(mode):
    if mode == 'cap':
       return cap
    if mode == 'cpC':
       return cpC
    if mode == 'para':
       return ''
    else:
       return ''  #punkt


def groupbyreg(txt,reg,mode,segmenter): 
      if mode=='punkt':
        return segment(txt,segmenter)

      if mode=='para':   # segmented by paragraphs, do not segment further
        return [txt] 

      else:
        chunks = []
        nxtchunk  = '' 
        def breakIt(match,nxtchunk,txt,chunks,mode):
           (st,end)    = match.span()
           (first,sec) = extractStartAndStop(match.group(),mode)
           chunk       = nxtchunk+txt[:st]+first
           chunks      += [chunk]
           nxtchunk    = sec
           txt         = txt[end:]
           return (nxtchunk,txt)
 
        while True:
          # look for § 1. 
          n = re.search(parastring,txt,flags=re.UNICODE)
          # if we find it, split here
          if n:
            (nxtchunk,txt) = breakIt(n,nxtchunk,txt,chunks,'cap')
          # else look for our normal sentence splitter
          else:
            m = re.search(reg,txt,flags=re.UNICODE)
            if m:
              (st,end)    = m.span()
              # roman numbers etc. can be ignored
              if not ignore(m.group(),mode):
                (nxtchunk,txt) = breakIt(m,nxtchunk,txt,chunks,mode)
              else: 
               nxtchunk = nxtchunk+ txt[:end]
               txt = txt[end:]
            else: 
               chunks += [nxtchunk+txt]
               break

        return chunks 

# defines which part of the stop-section that belong to the new vs. old sentence
# nltk span should not use the sentence counter. our should use it in some way?
def extractStartAndStop(s,x):
    if x=='cap':
       return ('',s)
    if x=='cpC':
       n = re.match(onlypunkt,s,flags=re.UNICODE)
       if n:   ## OBS change here to new
          (st,e) = n.span()
          return (s[:e],s[e:])
          #return (s[:-1],s[-1:])

# if roman number, don't count as capitalized
def ignore(string,mode):
    hasRoman = ()
    if mode=='cpC':
      punktRoman = punkt+u'('+pagenumbers+'u)*\s*'+romanpattern+'\s*$'
      hasRoman   = re.match(punktRoman,string,flags=re.U | re.I)
    if mode=='cap':
       hasRoman = re.match(startstring+romanpattern+'$',string,flags=re.U | re.I)
    return hasRoman is not None
    
    

################################################################################
# Regular expressions
################################################################################

# upper case letters
uppers = u"[ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖÞÆ]"

p1 = u'[\s>]#\s*[0-9]+'
p2 = u'\[\s*‡‡\s*[0-9]+\s*[abrv]*\s*\]'
p3 =      u'‡‡\s*[0-9]+[abrv]*'
pagenumbers = p1+'|'+p2+'|'+p3 

startstring = u'(^|\s)'
onlypunkt   = u'[.,¶]'
punkt       = u"[.,¶]\s*" 
parastring  = u'§\.*\s*[0-9]+\.*' # §. 1. 

cap = startstring+uppers+'\w*'
cpC = punkt+u'('+pagenumbers+u')*\s*'+uppers+'\w*'

# roman numbers, may use j instead of i. 
romanpattern = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IJ]X|[IV|V?[IJ]{0,3})'

#############################################################################
# For normal sentences, use nltk
#############################################################################

def segment(txt,segmenter):
    return segmenter.tokenize(txt)



