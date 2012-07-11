# -*- coding: utf-8 -*-
import re
from dltransl import edit_dist
from itertools import chain, combinations,islice,product
#from Queue import PriorityQueue         
#from math import fabs
import sys
import codecs
from pycons import pylist_to_conslist,suffix_conslist
import heapq
#import gc

"""Functions for calculating anagram values, finding spelling variations etc"""

"""
 rule based spell checking. applies edit distance
 spellchecksmall(word,hashlexicon,rules for variations)
 returns (False,(word,lemgram)) if the word is in the lexicon
 returns (True,(word,variant,distance,lemgram)) if variants are found
 returns (False,None) if nothing interesting is found
"""
def spellchecksmall(w,d,alpha,edit):
  #gc.collect()
  return getchanges(w,d,alpha,edit)
 

""" returns the hash value of character c
    if c is not a letter, the value is 0"""
def iso(c):
  v = 0
  #if c.isalpha() or c in bokstaver:
  # TODO this should be here if we expect weird chars in texts, not in lexicon..
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


def deltaize(rules):
  ret = []
  rules = sorted(rules,key=lambda rule: rule[0])

  curr_h, curr_w, curr_u = rules[0][0],rules[0][1],set([rules[0][2]]),
  for rule in rules[1:]:
    if rule[0] == curr_h:# and rule[1] == curr_w:
      curr_w = min(curr_w,rule[1])
      curr_u.add(rule[2])
    else:
      ret.append((curr_h,curr_w,list(set(curr_u))))
      curr_h, curr_w, curr_u = rule[0],rule[1],set([rule[2]])

  ret.append((curr_h,curr_w,list(set(curr_u))))

  ret = sorted(ret,key=lambda rule: rule[1])
  ret[0] = ret[0]+(0,0)
  for reti in xrange(1,len(ret)):
    ret[reti] = ret[reti]+(ret[reti-1][0],ret[reti-1][1])


  return ret 



""" adds the result, if any, to ccs"""
def addAll(res,ccs):
    ccs.extend(x for x in res.iteritems() if x not in ccs)

""" finds variations based on rules. any number of substitutions is allowed,
    but maximum 1000 variations are considered.
    getchanges(word,lexicon of anagram values,rules)"""
def getchanges(word,lex,changeset,edit): 

    ccs = []
    u,b,t = gettav(word,keep=True)
    av   = getav(word) 
    tavs = u+b+t
    ch   = []
    changesetget = changeset.get
    # substitutions only # TODO insertions and deletions? add '' for insertions?
    for (tav,involvedletters) in tavs:
      # get diff between tav and its translations
      ch.extend((x-tav,weigth,involvedletters) for (x,weigth) in changesetget(tav,[]))

#    ch.append((19254145824, 439587))

    ch = deltaize(ch)
    for bla in ch: 
      print bla
    #ch = sorted(ch,key=lambda x: (x[1],x[0]))
 
    lexget = lex.get
    print 'word',word,len(ch)
#    Dijkstra mode
    def countdijkstrafind(ch):
      edit_dist_cache = dict([])
      edit_dist_cachesetdefault = edit_dist_cache.setdefault
      for (hash_w,w) in dijkstrafind(pylist_to_conslist(ch),av,len(word)):
        ok = lexget(hash_w)
    #    print 'will add',ok,hash_w,w
        if ok:
         for (variantword,info) in ok.iteritems(): 
           dist = edit_dist_cachesetdefault((word,variantword),edit_dist(word,variantword,rules=edit[0],n=edit[1]))
           print 'word',word,variantword,'dist',dist,w
           if dist<=w+10:
             yield (variantword,info,dist)
      #gc.collect() # Togs bort nyss
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

  new_used = []
  while rules:
    new_used = list(set(used_position_filter(rules[0][2],used)))
#    new_used = list(set((x | y) for (x,y) in mproduct(rules[0][2],used) if not (x & y)))
    if new_used: 
      break
    rules = rules[1]

  return new_used,rules


def mproduct(iter1,iter2):
  for x in iter1:
    for y in iter2:
      yield x,y

def used_position_filter(rule_wished,used):
  for x in rule_wished:
    for y in used:
      if not x&y:
        yield x|y


def dijkstrafind(rules,originalhash,wlen):
  th = 2000000
  pq = []
  lheappop  = heapq.heappop
  lheappush = heapq.heappush
  lremove_run = remove_run

  w = 0
  lheappush(pq,(w,             # current cost
                [0],           # used letters 
                originalhash,  # current hash
                (),            # possible siblings
                rules,         # possible descendants
                0
                ))
  

  while pq:# and w < 2000000:
    (w,u,h,rs,rd,mu) = lheappop(pq)
    #print 'using',bin(u),'mother',mu
    #sys.getsizeof(pq)
    yield (h,w)
    # TODO just added eheheh
    #if len(pq)>13000000: 
    #  print 'breaking'
    #  break

    # create a descendant if any left
    nu,rd = lremove_run(rd,u)
    if rd and rd[0][1]+w <= th:
      d_hash,w_rule,w_useds,_,_ = rd[0]
      lheappush(pq,(w+w_rule,  
                    nu,
                    h+d_hash,
                    rd[1], # siblings
                    rd,    # descendants
                    u
                    )) 
    
    # create a sibling if any left
    if rs:
      #mu = u ^ rs[0][5]
      mw = w-rs[0][4]
      mh = h-rs[0][3]
      nu,rs = lremove_run(rs,mu)
      if rs and rs[0][1]+mw <= th:
        d_hash,w_rule,w_useds,_,_ = rs[0]
        lheappush(pq,(w_rule+mw,    
                      nu,
                      d_hash+mh,
                      rs[1],  # siblings
                      rs,  # descendants
                      mu
                      ))
  


