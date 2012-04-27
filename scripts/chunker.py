# -*- coding: utf_8 -*-
import re
import os
from usefuls import *
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
def byt(uri,out):
    fil = open(uri,'r').read()
    xml = etree.fromstring(fil)
    open(out,'w').write(etree.tostring(xml,encoding='utf-8'))

sentence_dir = '../sentenceinfo/thisisit/'


# reads files in sentence_dir and adds the correct encoding
def findmode(fil):
    def findFile(path):
      txt = open(path,'r').readlines()
      isInFile = False
      for line in txt:
          splitted = line.split()
          if splitted:
            if os.path.basename(splitted[0]) == os.path.basename(fil):
             isInFile = True
      return isInFile

    if findFile(os.path.join(sentence_dir,'dot.txt')):
      print fil,'punkt'
      return 'punkt'
    elif findFile(os.path.join(sentence_dir,'dotComma.txt')):
      print fil,'cpC'
      return 'cpC'
    elif findFile(os.path.join(sentence_dir,'paras.txt')):
      print fil,'para'
      return 'para'
    elif findFile(os.path.join(sentence_dir,'capital.txt')):
      print fil,'cap'
      return 'cap'
    else:
      print fil,'default'
      return 'punkt'


def putStops(xml,mode,segmenter):
#    fil = open(uri,'r').read()
#    xml = etree.fromstring(fil)
    print 'reading model...'

    body  = xml.find('body')
    sect  = body.find(prefix+'section').findall(prefix+'paragraph-definition')
    allPs = []
    for s in sect:
        allPs += s.iterfind('para')
    for para in allPs:
        segmenttext(para,mode,segmenter)
    return xml


#        txt = list(para.itertext())
#        if txt is not None and len(txt)>0:
#          ss.append(' '.join(txt))
#    ss = filter(lambda x : len(x.strip())>0,ss)
    #open(out,'w').write(etree.tostring(xml))

# segments all text in xml node
# returns list of sentences
def segmenttext(node,mode,segmenter):
    #txt = node.text
    txt = ''.join(list(node.itertext()))
    if txt is not None and len(txt.strip())>0:
      # clear all text
      node.text = ''
      for elem in node:
          elem.text = ''
      ss = groupbyreg(txt,regex(mode),mode,segmenter)
      for s in ss:
       sub = etree.SubElement(node, 's')
       sub.text = s

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
        while True:
          m = re.search(reg,txt,flags=re.UNICODE)
          if m:
            (st,end)    = m.span()
            if not ignore(m.group(),mode):
             (st,end)    = m.span()
             (first,sec) = extractStartAndStop(m.group(),mode)
             chunk       = nxtchunk+txt[:st]+first
             chunks      += [chunk]
             nxtchunk    = sec
             txt         = txt[end:]
            else: 
             nxtchunk = nxtchunk+ txt[:end]
             txt = txt[end:]
          else: 
             chunks += [nxtchunk+txt]
             break
        return chunks 

# defines which part of the stop-section that belong to the new vs. old sentence
def extractStartAndStop(s,x):
    if x=='cap':
       return ('',s)
    if x=='cpC':
       return (s[0],s[1:])

# if roman number, don't count as capitalized
def ignore(string,mode):
    hasRoman = ()
    if mode=='cpC':
      punktRoman = punkt+pagenumbers+'u)*\s*'+romanpattern+'\s*$'
      hasRoman   = re.match(punktRoman,string,flags=re.U | re.I)
    if mode=='cap':
       hasRoman = re.match(startstring+romanpattern+'$',string,flags=re.U | re.I)
    return hasRoman is not None
    
    

# upper case letters
uppers = u"[ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖÞÆ]"

p1 = u'[\s>]#\s*[0-9]+'
p2 = u'\[\s*‡‡\s*[0-9]+\s*[abrv]*\s*\]'
p3 =      u'‡‡\s*[0-9]+[abrv]*'
pagenumbers = p1+'|'+p2+'|'+p3 

startstring = u'(^|\s)'
punkt = u"[.,¶]\s*(" 
cap = startstring+uppers+'\w*'
cpC = punkt+pagenumbers+u')*\s*'+uppers+'\w*'

# roman numbers, may use j instead of i. 
romanpattern = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IJ]X|[IV|V?[IJ]{0,3})'

test =    punkt+pagenumbers+'u)*\s*'+romanpattern+'$'
#############################################################################
# For normal sentences, use nltk
#############################################################################

def segment(txt,segmenter):
    return segmenter.tokenize(txt)



