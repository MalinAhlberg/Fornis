# -*- coding: utf_8 -*-
# TODO ta med '' i tabellerna, lägg till n '' i ett n långt ord i cc
import re

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
 
""" finds the 'aav' alphabet, consisting of all strings, bigram and trigrams"""
def alphabet(wds):
    a =set([])
    for w in wds:
      u,b,t = gettav(w)
      map(lambda x: a.add(x),u+b+t)
    return a

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

""" gets character confusion set, the set of words comparable to this one
    transpositions or one substitution, deletion, insertion is allowed"""
def getccs((w,av),lex,alphabet,ccs=[]): 
    xs = lex.get(av) #transpositions
    addAll(xs,ccs)
    (u,b,t) = gettav(w)
    tavs = u+b+t
    for aav in alphabet: # deletions
      addAll(lex.get(av+aav),ccs)
      # substitutions
      [addAll(lex.get(av+aav-tav),ccs) for tav in tavs]
    # insertions
    [addAll(lex.get(av-tav),ccs) for tav in tavs]
    return ccs 
    
""" adds the result, if any, to ccs"""
def addAll(res,ccs):
    if res!=None:
      ccs += res.items() 

""" finds variations based on rules. any number of substitutions is allowed,
    but maximum 1000 variations are considered.
    getchanges(word,lexicon of anagram values,rules)"""
def getchanges(w,lex,changeset): 
    import codecs 
    ccs = []                    
    (u,b,t) = gettav(w,keep=True)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    # substitutions only
    # TODO add '' as aws (0's to the tav, how many?? as many as there are letters?)
    for tav in tavs+[0]*(len(w)/2):
      # get diff between tav and its translations
      subs = changeset.get(tav) or []
      ch += map(lambda x: x-tav,subs)

    # as we may get more than 2^31 combination, we only look at the 1000 first
    # variants. this has also proved to give as good results as trying all
    # combinations
    for (i,c) in enumerate(powerset(list(set(ch)))):
      ok = lex.get(av+sum(c))
      if ok:
        addAll(ok,ccs)
        found =True
      if i>1000:
        break
    return ccs


def powerset(iterable):
    from itertools import chain, combinations
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


