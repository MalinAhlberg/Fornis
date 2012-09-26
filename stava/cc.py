# -*- coding: utf-8 -*-
import pyximport; pyximport.install()
from hashfilter import dijkstrafind
import re
from dltransl import edit_dist
from itertools import chain, combinations,islice,product
import sys
import codecs
from pycons import pylist_to_conslist,suffix_conslist
import heapq
import gc
import operator
import time

"""Functions for calculating anagram values, finding spelling variations etc"""

"""
 rule based spell checking. applies edit distance
 spellchecksmall(word,hashlexicon,rules for variations)
 returns (False,(word,lemgram)) if the word is in the lexicon
 returns (True,(word,variant,distance,lemgram)) if variants are found
 returns (False,None) if nothing interesting is found
"""
def spellchecksmall(w,d,alpha,edit):
  if len(w)>32:
    print 'word',w,'discarded'
    return ''  #TODO return something better
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


bokstaver = u'åäöÅÄÖæÆøØÞþßÇ^$àáçèéêëíîïóôûüÿᛘ∂' # obs ^ and $ here to mark end beginning of words
 
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

def add_with_subsumption_check(olds,new):

  ret = []

  for oldi,old in enumerate(olds):
    old_or_new = old | new
    if old_or_new == new:
      # this information is already here
      # copy all and exit loop
      ret.extend(olds[oldi:])
      break
    elif old_or_new == old:
      # the new info is more general
      # do not copy the old info
      pass
    else:
      # copy the old info
      ret.append(old)
  else:
    # only when not breaked --> need to add new info
    ret.append(new)

  return ret


def subsumption_filter(bitmaps):

  bitmaps = sorted(bitmaps)
  rets = []

  for bitmap in bitmaps:
    for ret in rets:
      if (ret | bitmap) == bitmap:
        break
    else:
      rets.append(bitmap)

  return rets

def deltaize(rules):
  ret = []
  rules = sorted(rules,key=lambda rule: rule[0])

  curr_h, curr_w, curr_u = rules[0][0],rules[0][1],[rules[0][2]],
  for rule in rules[1:]:
    if rule[0] == curr_h:# and rule[1] == curr_w:
      curr_w = min(curr_w,rule[1])
      curr_u.append(rule[2])
    else:
      ret.append((curr_h,curr_w,subsumption_filter(curr_u)))
      curr_h, curr_w, curr_u = rule[0],rule[1],[rule[2]]

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

    t0 = time.clock()
    ccs = []
    u,b,t = gettav(word,keep=True)
    av   = getav(word) 
    # TODO fix!
    if av >= 50014198618560734057L:
      print 'discarded, too long hash',word,av 
      return ()
    tavs = u+b+t
    ch1   = []
    changesetget = changeset.get
    # substitutions only # TODO insertions and deletions? add '' for insertions?
    for (tav,involvedletters) in tavs:
      # get diff between tav and its translations
      ch1.extend((x-tav,weigth,involvedletters) for (x,weigth) in changesetget(tav,[]))


    ch = deltaize(ch1)
    
    print 'word',word,len(ch1),len(ch),

    bla = countdijkstrafind(ch,word,edit,lex,av)
    print 'word-time',time.clock()-t0,'(',len(word),' letters)'
    print bla
    print '***', '  '.join([x[2][0] for x in bla])
    print '\n\n'
    return bla


#    Dijkstra mode
def countdijkstrafind(ch,word,edit,lex,av):
 # stuff for kbest list
 th = 2000000
 k = 3
 seen = set([])
 topklist = [(th+1,0,())]*k
 lexget = lex.get

 for (hash_w,w,iters) in dijkstrafind(ch,av,len(word),th):
   if topklist[-1][2] and topklist[-1][0] < w:
     break
       
   ok = lexget(hash_w,{})
   for (variantword,info) in ok.iteritems():
     if not variantword in seen:
       dist,eds = edit_dist(word,variantword,rules=edit[0],n=edit[1])
       seen.add(variantword)
       topklist.append((dist,eds,(variantword,info)))
       topklist = sorted(topklist)[:k]
       print
       print variantword, w, dist,eds,
     else:
       print '.',

 topklist = filter(lambda (x,z,y): y!=(),topklist)
 print
 print 'iterations',iters,'edits',len(seen)
 print 'found',len(topklist)
 print
 return topklist


def remove_run(rules,used):

  new_used = []
  while rules:
    new_used = list(new_sub_filter(used_position_filter(rules[0][2],used)))
    if new_used: 
      break
    rules = rules[1]

  return new_used,rules


def used_position_filter(rule_wished,used):
  for x in rule_wished:
    for y in used:
      if not x&y:
        yield x|y


def new_sub_filter(bitmaps):
  for x in bitmaps:
    if not any((x | y)==x for y in bitmaps):
      yield x


#def dijkstrafind(rules,originalhash,wlen,th):
#  pq = []
#  lheappop  = heapq.heappop
#  lheappush = heapq.heappush
#  lremove_run = remove_run
#
#  w = 0
#  lheappush(pq,(w,             # current cost
#                [0],           # used letters 
#                originalhash,  # current hash
#                (),            # possible siblings
#                rules,         # possible descendants
#                0))
#  
#
#  while pq:# and w < 2000000:
#    (w,u,h,rs,rd,mu) = lheappop(pq)
#    yield (h,w)
#
#    # create a descendant if any left
#    nu,rd = lremove_run(rd,u)
#    if rd and rd[0][1]+w <= th:
#      
#      d_hash,w_rule,w_useds,_,_ = rd[0]
#      lheappush(pq,(w+w_rule,  
#                    nu,
#                    h+d_hash,
#                    rd[1],    # siblings
#                    rd,       # descendants
#                    u,
#                    )) 
#    
#    # create a sibling if any left
#    if rs:
#      mw = w-rs[0][4]
#      mh = h-rs[0][3]
#      nu,rs = lremove_run(rs,mu)
#      if rs and rs[0][1]+mw <= th:
#        d_hash,w_rule,w_useds,_,_ = rs[0]
#        lheappush(pq,(mw+w_rule,    
#                      nu,
#                      mh+d_hash,
#                      rs[1],   # siblings
#                      rs,      # descendants
#                      mu
#                      ))
#  





# graveyard


def mproduct(iter1,iter2):
  for x in iter1:
    for y in iter2:
      yield x,y
