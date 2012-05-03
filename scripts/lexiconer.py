# -*- coding: utf_8 -*-
import re
import os
import glob
import codecs
from xml.etree import ElementTree as etree

# read file and return list of entries and reference to the whole lexicon
def readIt(fil):
     s = open(fil, "r").read()
     lexicon = etree.fromstring(s)
     lex     = lexicon.find('Lexicon')
     entries = lex.findall('LexicalEntry')
     return (entries,lexicon)

# prints words that (easily) refers to others
# saves the updated version, with replaced tags for successful e-words
# to file if 'saves' is set to true.
def references():
    errFile = 'error.txt'
    saves   = True # False # 
    lexicon = '../../Lexicon/schlyter.xml' #'../../Lexicon/test.xml' 'testRef2.xml' #
    outFile = 'testRef3.xml'
    refFile = 'refer.txt'
    open(refFile,'w').write('') # empty old references


    def run(lexicon,outFile,i):
        print 'round',i
        errs = [] # empty errors
        lst  = []
        print 'reading',lexicon
        (entries,lex) = readIt(lexicon)
        for entry in entries: 
            (pos,l) = getTag(entry)
            (lem,_) = getAtt(getFormRepresentation(entry),lemgram)[0]
            # if it is has an e tag, try to fix it
            if pos == 'e':
              ref = findReference(l,entry,entries,errs,save=saves)
              if ref is not None: lst.append((lem,ref))
        if saves:
          print 'writing lexicon',outFile
          open(outFile,'w').write(etree.tostring(lex,encoding='utf-8'))
        print 'new references',len(lst)
        codecs.open(refFile,'a','utf-8').write(format(lst))
        updates = len(lst)
        print 'errors',len(errs)
        if saves and updates != 0:
           print 'rerunning...'
           return run(outFile,'rerunlex'+str(i)+'.xml',i+1)
        else: return errs

    def format(lst):
        ss = ''
        for (a,b) in lst:
            ss += a+'\t'+b+'\n'
        return ss
    err = run(lexicon,outFile,0)
    codecs.open(errFile,'w','utf-8').write('\n'.join(err))
       
        

# replaces e:s with pos-tags from gram-information
def makeTags():
    (entries,lex) = readIt('../../Lexicon/schlyter.xml')
    counter =  []
    for entry in entries: 
        (tag,elem) = getTag(entry)
        if not tag or tag =='e':
           setNewTag(elem,entry,counter)
    open('testL.xml','w').write(etree.tostring(lex,encoding='utf-8'))
    print len(counter)

# lexical entry -> form representation       
def getFormRepresentation(entry):
    lemma = entry.find('Lemma')
    form  = lemma.find('FormRepresentation')
    return form

# lexical entry -> (pos-tag, element containing pos-tag)
def getTag(entry):
    form  = getFormRepresentation(entry)
    lems  = getAtt(form,lemgram)
    return extractTag(lems)

# lem -> (pos-tag, element containing pos-tag)
def extractTag(lem):
    if lem is not None:
        (tag,elem) = lem[0]
        return (tag.split('.')[2],elem)
    else: return (None,None)

# lexical entry -> lemgram
def getLem(entry):
    form  = getFormRepresentation(entry)
    lems  = getAtt(form,lemgram)
    return extractLem(lems)

# lem -> lemgram-id
def extractLem(lem):
    if lem is not None:
        (tag,elem) = lem[0]
        return tag
    else: return ""

# check if there is unmatched paranthesis in hwtext
def checkHW(fil):
    (entries,_) = readIt('../../Lexicon/schlyter.xml')
    for entry in entries: 
         findHW(entry)

# lexical entry -> print if there's unmatched paranthesis
def findHW(lem):
    form = getFormRepresentation(lem)
    lems  = getAtt(form,'hwtext')
    (l,_) = getAtt(form,lemgram)[0]
    for (hw,x) in lems:
        #print hw
        if countP(hw)!=0:
          print hw
          print l
     
# searches for information about references. 'lem' is the lemgram where the
# information should be saved, 'entry' the whole entry, 'lex' the whole lexicon
def findReference(lem,entry,lex,errs,save=False):
   # kolla om det står se i Sense -Definition - text
    sense  = entry.find('Sense')
    if not sense is None:
      info   = sense.find('Definition')
      if not info is None:
        texts  = getAtt(info,'text')
        for (txt,elem) in texts:
            words = txt.strip(' .').split(',')
             # isf slå upp ord (liten bokstav), om det bara finns ett alternativ
            if words and words[0].startswith('se ') and len(words)==1:
              lems = lookup(normalize(words[0]),lex,'writtenForm') # writtenform also for multiwords?
              # finns det bara en, visa den
              if len(lems)==1:
                (pos,_) = getTag(lems[0])
                if pos != 'e':
                   (reflem,_) = getAtt(getFormRepresentation(lems[0]),lemgram)[0]
                   if save:
                     lem.set('val',re.sub('\.\.e\.','..'+pos+'.',lem.get('val')))
                   return reflem
                else: errs += ['refererence to "e" '+lem.get('val')+' '+txt]
              else: errs += ['too many or few references '+str(len(lems))+' '+txt]
            elif words and words[0]=='se': 
              errs += ['bad reference '+txt]

def normalize(words):
    return (words[3:]).lower()  # remove 'se '

def lookup(e,lex,typ):
    res = []
    for entry in lex:
        form = getFormRepresentation(entry)
        eres = getAtt(form,typ)
        for (txt,elem) in eres:
            if txt==e:
              res.append(entry)
    return res



def setNewTag(elem,entry,counter):
    form = getFormRepresentation(entry)
    (l,_) = getAtt(form,lemgram)[0]
    txt   = getAtt(form,'gram')
    old = elem.get('val')
    for (t,_) in txt:
        if isNoun(t):
           print 'nn',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..nn.',old))
        if isPrep(t):
           print 'prep',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..pp.',old))
        if isAdj(t):
           print 'adj',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..av.',old))
        if isVerb(t):
           print 'vb',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..vb.',old))
        if isAdv(t):
           print 'adv',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..ab.',old))
        if isConj(t):
           print 'conj',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..kn.',old))

# only in beginning of string? other word classes
def isNoun(t):
  return t.startswith('n.') or t.startswith('f.') or t.startswith('m.')
def isPrep(t):
  return t.startswith(u'præp.')
def isAdj(t):
  return t.startswith('adj.')
def isAdv(t):
  return t.startswith('adv.')
def isVerb(t):
  return t.startswith('v.')
def isConj(t):
  return t.startswith('conj.')

# gets the value of 'val' in 'elem'
def getAtt(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append((feat.get('val'),feat))
    return res
    
# count number of paranthesis
def countP(w):
   i=0
   for c in w:
       if c=='(':
         i = i+1
       if c==')':
         i = i-1
   return i              

def countE(fil):         
    (entries,lex) = readIt(fil)
    counter = 0
    for entry in entries: 
        (pos,l) = getTag(entry)
        if pos == 'e':
           counter += 1
    print fil,"number of 'e's",counter


from collections import Counter
def printPOS(fil):
    (entries,lex) = readIt(fil)
    poss = []
    for entry in entries: 
        (pos,l) = getTag(entry)
        poss.append(pos)
    print Counter(poss)

def getGrams(fils):
    grams = []
    for fil in fils:
      (entries,lex) = readIt(fil)
      for entry in entries: 
          form = getFormRepresentation(entry)
          (l,_) = getAtt(form,lemgram)[0]
          txt   = getAtt(form,'gram')
          for (t,_) in txt:
              grams.append(t)
    print Counter(grams)

def checklemgrams(fils):
    grams = []
    for fil in fils:
      (entries,lex) = readIt(fil)
      for entry in entries: 
        l = getLem(entry)
        if '*' in l or '?' in l:
           grams.append(l) 
    print grams

lemgram = 'lemgram' # 'lem'
# checklemgrams(['../../Lexicon/soederwall_ny/soederwall_main_ONSDAG.xml','../../Lexicon/soederwall_ny/soederwall_supp_ONSDAG.xml'])

