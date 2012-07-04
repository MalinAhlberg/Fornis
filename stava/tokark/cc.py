# -*- coding: utf_8 -*-
import re
from itertools import chain, combinations,islice
import sys
import codecs

"""Functions for calculating anagram values, finding spelling variations etc"""

""" returns the hash value of character c
    if c is not a letter, the value is 0"""
def iso(c):
  v = 0
  if c.isalpha() or c in bokstaver:
    v = ord(c.lower())
  return pow(v,5)

""" returns the hash value of a word
    ie the sum all the hash value of each character"""
def hashiso(w):
    return sum([iso(c) for c in w])
 
""" normalize a word by removing all but letters"""
def norm(w):
    return re.sub(u'[^\w'+bokstaver+']','',w)

bokstaver = u'åäöÅÄÖæÆøØÞþß^$' # obs ^ and $ here to mark end beginning of words

""" gets the av:s for a word. if keep is set to True, the beginning and end
    of the word is marked by ^ vs $. Otherwise _ are added, to avoid that
    the first and the last letter is unbenefitted """
def gettav(w,keep=False):
    sw = '^'+w+'$' if keep else '_'+w+'_'
    unis = [iso(w[i]) for i in range(len(w))]
    bis = [iso(sw[i])+iso(sw[i+1]) for i in range(len(w)+1)]
    tris = []
    if len(w)>5:
      tris =  [iso(sw[i])+iso(sw[i+1])+iso(sw[i+2]) for i in range(len(w))]
    return unis,bis,tris
   
""" adds the result, if any, to ccs"""
def addAll(res,ccs):
    ccs.extend(x for x in res.iteritems() if x not in ccs)

""" finds variations based on rules. any number of substitutions is allowed,
    but maximum 1000 variations are considered.
    getchanges(word,lexicon of anagram values,rules)"""
def getchanges(w,lex,changeset): 
    print 'word',w
    ccs = []
    (u,b,t) = gettav(w,keep=True)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    changesetget = changeset.get
    # substitutions only # TODO insertions and deletions? add '' for insertions?
    for tav in tavs:
      # get diff between tav and its translations
      ch.extend((x-tav,weigth) for (x,weigth) in (changesetget(tav) or []))
    lexget = lex.get

    # as we may get more than 2^31 combination, we only look at the 1000 first
    # variants. this has also proved to give as good results as trying all combinations

    ch = [a for (a,b) in sorted(set(ch),key=lambda (x,v):v)]# sort this to get good changes first
    def countpowerfind(ch):
      tested = []
      for c in islice(powerset(ch),0,1000000): #need a limit here, otherwise will get stuck (gräßhoppor)
        sumc = sum(c)
        ok = lexget(av+sumc)
        if ok and not sumc in tested:
          #print 'succes for',sumc,'got',ok
          yield ok
          tested.append(sumc)
          addAll(ok,ccs)

    for ok in islice(countpowerfind(ch),0,100): # only need to send 100 to edit distance
        addAll(ok,ccs)
    return ccs

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


