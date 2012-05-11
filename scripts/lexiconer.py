# -*- coding: utf_8 -*-
import re
import os
import glob
import codecs
from xml.etree import ElementTree as etree
from xmlindent import indent

# read file and return list of entries and reference to the whole lexicon
def readIt(fil):
     s = codecs.open(fil,"r").read()
     lexicon = etree.fromstring(s)
     print type(lexicon)
     #lexicon = lexicon.getroot()
     indent(lexicon)
     lex     = lexicon.find('Lexicon')
     entries = lex.findall('LexicalEntry')
     return (entries,lexicon)

# prints words that (easily) refers to others
# saves the updated version, with replaced tags for successful e-words
# to file if 'saves' is set to true.
def references():
    errFile = 'error.txt'
    saves   = True # False # 
    lexicon = currentfile
    outFile = 'testRef3.xml'
    refFile = 'refer.txt'
    open(refFile,'w').write('') # empty old references
    dlex  = mkLex(keeppos=False)


    def run(lexicon,outFile,i,dlex):
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
              ref = findReference(l,entry,dlex,errs,save=saves)
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
           return run(outFile,'rerunlex'+str(i)+'.xml',i+1,dlex)
        else: return errs

    def format(lst):
        ss = ''
        for (a,b) in lst:
            ss += a+'\t'+b+'\n'
        return ss
    err = run(lexicon,outFile,0,dlex)
    codecs.open(errFile,'w','utf-8').write('\n'.join(err))
       
        

# replaces e:s with pos-tags from gram-information
def makeTags():
    (entries,lex) = readIt('rerunlex0.xml')
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
    #form  = getFormRepresentation(entry)
    lemma = entry.find('Lemma')
    lems  = getAtt(lemma,lemgram)
    return extractTag(lems)

# lem -> (pos-tag, element containing pos-tag)
def extractTag(lem):
    if lem is not None:
        (tag,elem) = lem[0]
        return (tag.split('.')[2],elem)
    else: return (None,None)

# lexical entry -> lemgram
def getLem(entry):
    #form  = getFormRepresentation(entry)
    lemma = entry.find('Lemma')
    lems  = getAtt(lemma,lemgram)
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
# information should be saved, 'entry' the whole entry, 'lex' the dictionary
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
              (_,lems) = lookupLex(normalize(words[0]),lex) #,'writtenForm') # writtenform also for multiwords?
              # finns det bara en, visa den
              if len(lems)==1:
                #(pos,_) = getTag(lems[0])
                pos = lems[0].get('pos')
                if pos != 'e':
                   reflem = lems[0].get('lemgram')
                   #(reflem,_) = getAtt(getFormRepresentation(lems[0]),lemgram)[0]
                   if save:
                     lem.set('val',re.sub('\.\.e\.','..'+pos+'.',lem.get('val')))
                   return reflem
                else: errs += ['refererence to "e" '+lem.get('val')+' '+txt]
              else: errs += ['too many or few references '+str(len(lems))+' '+txt]
            elif words and words[0]=='se': 
              errs += ['bad reference '+txt]

def normalize(words):
    word = words[3:].lower().strip('.,()')  # remove 'se '
    words = word.split()
    if len(words)<3:
       word = '_'.join(words)
    return word


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
        elif isPrep(t):
           print 'prep',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..pp.',old))
        elif isAdj(t):
           print 'adj',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..av.',old))
        elif isVerb(t):
           print 'vb',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..vb.',old))
        elif isAdv(t):
           print 'adv',l
           counter.append(0)
           elem.set('val',re.sub('\.\.e\.','..ab.',old))
        elif isConj(t):
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

def getAttRef(elem,val):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res += [feat]
    return res

# gets triples of children. elem -> (att,val,reference)
def getAll(elem,skip=[]):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value not in skip:
             res.append((value,feat.get('val'),feat))
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
    number  = 0
    for entry in entries: 
        (pos,l) = getTag(entry)
        #lemma = entry.find('Lemma')
        #lems    = getAtt(lemma,lemgram)
        #(pos,l) = extractTag(lems)
        if pos == 'e':
           counter += 1
        number += 1
    print fil,"number of 'e's",counter,'(',number,')'


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
           grams.append((l,fil)) 
    print grams

def duplicatelems():
    lems = []
    for fil in files:
      entries,_ = readIt(fil) 
      for entry in entries:
        lems   += [getLem(entry)]
#    lines = codecs.open('lexiconinfo/badlemsSoederNY.txt','r','utf-8').readlines()
    lex   = mkLex()
    dups  = []
    for word in lems:
#    for line in lines:
#        word = line.split()[0]
#        word = word.strip("',")
        (l,xs) = lookupLex(word,lex)
        if xs is None or xs==[]:
          print 'error, could not find',word
        elif len(xs)>1:
          dups += [(l,xs)]
    print dups

def lookupLex(word,lex):
    lem = re.sub('\*|\?','',word)
    res = lex.get(lem) if lex.has_key(lem) else 0 #[] OBS TODO fix this, should be the rigth type
    return (lem,res)

allfiles = [soederwall_main, soederwall_supp, schlyter]
def mkLex(keeppos=True,files=allfiles,numbers=False):
    print 'reading files'
    lex = {}
    print 'making lexicon'
    for fil in files: 
      entries,_ = readIt(fil) 
      for entry in entries:
        lem     = getLem(entry)
        lemgram = lem
        if not keeppos:
          lem = lem.split('.')[0]
        pos,_ = getTag(entry)
        lem1 = re.sub('\*|\?','',lem)
        standard  = [{"form": lem, "file" : fil, "pos" : pos, 'lemgram' : lemgram}]
        attr  = 1 if numbers else standard
        if lex.has_key(lem1):
           old = lex.get(lem1)
           attr = old + attr
        lex.update({lem1 : attr})
    print 'lexicon complete'
    return lex

soederwall_main = '../../Lexicon/soederwall_ny/soederwall_main_NYAST.xml'
soederwall_supp = '../../Lexicon/soederwall_ny/soederwall_supp_NYAST.xml'
schlyter        = '../../Lexicon/schlyter.xml'
currentfile= schlyter
    
# def organizer()
# fixar så att 
# -om namnet finns i annan ordbok så får den ett nytt id
# -om lemgram, sense:id eller writtenform har '?' eller '*' eller '('
#   så ta bort dem, lägg gamla namnet i oldForm 
# om annat dåligt tecken i nån av dem, rapportera



lemgram = 'lemgram' # 'lem'
#checklemgrams(['../../Lexicon/soederwall_ny/soederwall_main_NYAST.xml'
#                ,'../../Lexicon/soederwall_ny/soederwall_supp_NYAST.xml'])
#duplicatelems()

