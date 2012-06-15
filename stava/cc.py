# -*- coding: utf_8 -*-
import re
from dltransl import edit_dist
from itertools import chain, combinations,islice
import sys

"""Functions for calculating anagram values, finding spelling variations etc"""


"""
combines rules with 'normal' spelling variation. applies edit distance
spellcheckword(word,hashlexicon,rules for variations,alphabet of common hash-grams)
returns (False,(word,lemgram)) if the word is in the lexicon
returns (True,(word,variant,distance,lemgram)) if variants are found
returns (False,None) if nothing interesting is found
"""
def spellcheckword(w,d,rules,a): 

  lem = getlemgram(d,w)
  if lem==None:
    ccs    = []
    cc = []
    getccs((w,hashiso(w)),d,a,cc)
    ccs.append((w,set(cc)))
    # allowed dist should depend on wordlength?
    res = getvariant(ccs)
    if res:
      return (True,res)
  else:
    return (False,(w,lem))

  # False,None implies it was in dict but we didn't get good spelling variants
  return (False,None)

"""
 rule based spell checking. applies edit distance
 spellchecksmall(word,hashlexicon,rules for variations)
 returns (False,(word,lemgram)) if the word is in the lexicon
 returns (True,(word,variant,distance,lemgram)) if variants are found
 returns (False,None) if nothing interesting is found
"""
def spellchecksmall(w,d,alpha,edit):
  ccs = [(w,getchanges(w,d,alpha))]
  res,j = getvariant(ccs,edit)
  # with codecs.open('howmanykast','a',encoding='utf8') as f:
  #   f.write(w+' '+str(j)+'\n')
  if res==None:
    return (False,None)
  else:
    return (True,res)
 
 
""" Examines a set of words and their variations and picks
    the ones that has an accepteble edit distance (2)
    returns a list of (word,variation,edit distance,lemgram)"""
def getvariant(ccs,edit):
  from math import fabs
  var = []
  j = 0
  for (w,cc) in ccs:
    for (c,lem) in dict(cc).items():
      if fabs(len(w)-len(c))<=len(w)/2:
        dist = edit_dist(w,c,rules=edit[0],n=edit[1]) if edit else edit_dist(w,c) 
        j+=1
        if dist<2:
          var.append((w,c,dist,lem))
  var.sort(key=lambda (w,c,dist,lem): dist)
  return (var,j)


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
   
""" adds the result, if any, to ccs"""
def addAll(res,ccs):
    ccs.extend(x for x in res.iteritems() if x not in ccs)

""" finds variations based on rules. any number of substitutions is allowed,
    but maximum 1000 variations are considered.
    getchanges(word,lexicon of anagram values,rules)"""
def getchanges(w,lex,changeset): 
    ccs = []
    (u,b,t) = gettav(w,keep=True)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    changesetget = changeset.get
    # substitutions only # TODO insertions and deletions? add '' for insertions?
    for tav in tavs:
      # get diff between tav and its translations
      ch.extend((x-tav,val) for (x,val) in (changesetget(tav) or []))


    ch = [a for (a,b) in sorted(set(ch),key=lambda (x,v):v)]# sort this to get good changes first
    # as we may get more than 2^31 combination, we only look at the 1000 first
    # variants. this has also proved to give as good results as trying all combinations
    lexget = lex.get
    for c in islice(powerset(ch),0,100000):
      ok = lexget(av+sum(c))
      if ok:
        addAll(ok,ccs)
    return ccs


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


# For statistical spellchecking
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
 
