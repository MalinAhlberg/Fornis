# -*- coding: utf-8 -*-
import re
from dltransl import edit_dist
from itertools import chain, combinations,islice
#from Queue import PriorityQueue         
#from math import fabs
import sys
import codecs
from pycons import pylist_to_conslist,suffix_conslist
import heapq

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
  #import gc
  #gc.collect()
  return getchanges(w,d,alpha,edit)
 
 
""" Examines a set of words and their variations and picks
    the ones that has an accepteble edit distance (2)
    returns a list of (word,variation,edit distance,lemgram)"""
def getvariant(ccs,edit,distance=2):
  var = []
  j = 0
  print 'ccs is',ccs
  for (w,cc) in ccs:
    for (c,lem) in dict(cc).items():
#      if fabs(len(w)-len(c))<=len(w)/2:
        dist = edit_dist(w,c,rules=edit[0],n=edit[1]) if edit else edit_dist(w,c) 
        j+=1
        if dist<distance:
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

bit0   = 0
bit1   = 1
""" gets the av:s for a word. if keep is set to True, the beginning and end
    of the word is marked by ^ vs $. Otherwise _ are added, to avoid that
    the first and the last letter is unbenefitted
    word => [(av,letters involved)]"""
def gettav(w,keep=False):
    sw   = '^'+w+'$' if keep else '_'+w+'_'
    unis = [(iso(c),bit1<<i) for (i,c) in enumerate(sw)]
    bis  = [(iso(wi)+iso(wj),bit1<<i | bit1<<i+1) for (i,(wi,wj)) in enumerate(zip(sw[:-1],sw[1:]))]
    tris = [(iso(wi)+iso(wj)+iso(wk),bit1<<i | bit1<<i+1 |  bit1<<i+2) 
                      for (i,(wi,wj,wk)) in enumerate(zip(sw[:-2],sw[1:-1],sw[2:]))]

    return unis,bis,tris
   
def getav(w):
  return sum([iso(c) for c in w])

"""
[(d_hash1,w_rule1,involvedletters1),(d_hash2,w_rule2,involvedletters2),...]
=>
[(d_hash1,w_rule1,involvedletters1,d_hash1,w_rule1,0),(d_hash2,w_rule2,involvedletters2,d_hash2-d_hash1,w_rule2-w_rule1,involvedletters1),...]
"""
def deltaize(rules):
  ret = []

  rule0  = (0,0,0) 
  for rule in rules:
    if not rule == rule0:
      ret.append( (rule[0], rule[1],rule[2],rule[0]-rule0[0], rule[1] - rule0[1],rule0[2]) )
      drule0 = (rule[0]-rule0[0], rule[1] - rule0[1])
      rule0 = rule      

  # borde ej behövas mer
    else:
      ret.append( (rule[0], rule[1], rule[2],drule0[0], drule0[1],bit0 )) # a xor 0 = a , så att använda bokstäver behålls vid likadant syskon


  return ret

""" adds the result, if any, to ccs"""
def addAll(res,ccs):
    ccs.extend(x for x in res.iteritems() if x not in ccs)

""" finds variations based on rules. any number of substitutions is allowed,
    but maximum 1000 variations are considered.
    getchanges(word,lexicon of anagram values,rules)"""
def getchanges(word,lex,changeset,edit): 
    print 'word',word
#    for bla in changeset.iteritems():

    ccs = []
    u,b,t = gettav(word,keep=True)
#    print (u,b,t)
    av   = getav(word) 
    tavs = u+b+t
    ch   = []
    changesetget = changeset.get
    # substitutions only # TODO insertions and deletions? add '' for insertions?
    for (tav,involvedletters) in tavs:
      # get diff between tav and its translations
      ch.extend((x-tav,weigth,involvedletters) for (x,weigth) in changesetget(tav,[]))

#    ch.append((19254145824, 439587))

    #ch = deltaize(sorted(ch,key=lambda x: (x[1],x[0])))
    ch = sorted(ch,key=lambda x: (x[1],x[0]))
 
    lexget = lex.get
#    Dijkstra mode
    def countdijkstrafind(ch):
    #  tested = []
      edit_dist_cache = dict([])
      edit_dist_cachesetdefault = edit_dist_cache.setdefault
      for (hash_w,w) in dijkstrafind(pylist_to_conslist(ch),av,len(word)):
        ok = lexget(hash_w)
    #    print 'will add',ok,hash_w,w
        if ok: # and not c in tested:
         for (variantword,info) in ok.iteritems(): # if x not in ccs:
           dist = edit_dist_cachesetdefault((word,variantword),edit_dist(word,variantword,rules=edit[0],n=edit[1]))
           print 'word',word,variantword,'dist',dist,w
           #tested.append(c)
           if dist<=w+10:
             yield (variantword,info,dist)
      yield ('',[],-1)

#    print 'lexicon',sys.getsizeof(lex)
#    print 'edit',sys.getsizeof(edit)
#    print 'ch',sys.getsizeof(ch)
    for x in countdijkstrafind(ch):
      if x not in ccs:
        print x
        ccs.append(x)
        if len(ccs) >= 3:
          break
      
    return ccs

def remove_run(rules,used):
  while rules and (rules[0][2] & used)!=bit0:
    rules = rules[1]

  return rules


def dijkstrafind(rules,originalhash,wlen):
  pq = []
  lheappop  = heapq.heappop
  lheappush = heapq.heappush
  lremove_run = remove_run

  w = 0
  lheappush(pq,(w,             # current cost
                0,             # used letters 
                (),        # possible siblings
                #((),0),        # possible siblings
                #(rules,0),     # possible descendants
                rules,     # possible descendants
                originalhash,  # current hash
                0,0,originalhash   # mother node
                ))

  while pq and w < 2000000:
    (w,u,rs,rd,h,mw,mu,mh) = lheappop(pq)
#    print w,h
    #print 'using',bin(u),'mother',mu
    yield (h,w)

    # create a descendant if any left
    rd = lremove_run(rd,u)
    if rd:
      d_hash,w_rule,w_used = rd[0]
      used = u | w_used
      lheappush(pq,(w+w_rule,  
                    used, 
                    #lremove_run(rd[1],u),    # siblings
                    #lremove_run(rd[1],used), # descendants
                    rd[1],    # siblings
                    rd[1], # descendants
                    #(rd[1],u),    # siblings
                    #(rd[1],used), # descendants
                    h+d_hash,
                    w,u,h
                    )) 
    
    # create a sibling if any left
    # TODO START bättre (snabbare) men ej bra nog
    rs = lremove_run(rs,mu)
    if rs:
      d_hash,w_rule,w_used = rs[0]
      used = mu | w_used           
      lheappush(pq,(mw+w_rule,    
                    used,
                    #lremove_run(rs[1],mu),    # siblings,
                    #lremove_run(rs[1],used),  # descendants,
                    #(rs[1],mu),  # siblings
                    #(rs[1],used),  # descendants
                    rs[1],  # siblings
                    rs[1],  # descendants
                    mh+d_hash,
                    mw,mu,mh))



#def dijkstrafind(rules,originalhash,wlen):
#  pq = []
#  lheappop  = heapq.heappop
#  lheappush = heapq.heappush
#  lheappush(pq,(0,rules,originalhash))
#
#  while pq:
#    (w,r,h) = lheappop(pq)
#    last = (0,0)
#    #print sys.getsizeof(pq)
#    yield (h,w)
#    if w>3: break
#    #print 'next\n'
#    for suffix in suffix_conslist(r):
#      if not suffix[0] == last:
#        (d_hash,w_rule) = last = suffix[0]
#        #print 'add suffixes',suffix[1]
#        lheappush(pq,(w+w_rule,suffix[1],h+d_hash))


def setprio(p,i,x):
  p[i] = x 

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


# ska vara i getchanges
    # as we may get more than 2^31 combination, we only look at the 1000 first
    # variants. this has also proved to give as good results as trying all combinations

################################################################################
#    Power mode
 #   ch = [a for (a,b) in sorted(set(ch),key=lambda (x,v):v)]# sort this to get good changes first
 #   def countpowerfind(ch):
 #     tested = []
 #     for c in islice(powerset(ch),0,1000000): #need a limit here, otherwise will get stuck (gräßhoppor)
 #       sumc = sum(c)
 #       ok = lexget(av+sumc)
 #       if ok and not sumc in tested:
 #         #print 'success for',sumc,'got',ok
 #         yield ok
 #         tested.append(sumc)
 #         addAll(ok,ccs)
 #
 #   for ok in islice(countpowerfind(ch),0,100): # only need to send 100 to edit distance
 #       addAll(ok,ccs)
 #   return ccs
################################################################################

################################################################################

