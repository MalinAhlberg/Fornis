# -*- coding: utf_8 -*-
from normalize import iso,hashiso

"""Functions for calculating anagram values, finding spelling variations etc"""

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
    #found = False
    # substitutions only
    for tav in tavs:
      # get diff between tav and its translations
      subs = changeset.get(tav) or []
      ch += map(lambda x: x-tav,subs)

    # as we may get >2^31 combination, we only look at the 30 first variants and
    # continue only if we haven't found anything useful. 
    #i = 0
    for (i,c) in enumerate(powerset(list(set(ch)))):
      ok = lex.get(av+sum(c))
      if ok:
        addAll(ok,ccs)
        found =True
      if i>1000: #found or i> 1000000:
        break
    #[addAll(lex.get(av+sum(c)),ccs) for c in powerset(set(ch)) if av+sum(c)>0]
    #if i>200:
    #  codecs.open('reskast1','a',encoding='utf8').write(' '.join(['\n',w,unicode(i),unicode(found)]))
    return ccs

def powerset(iterable):
    from itertools import chain, combinations
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

####### CAN BE REMOVED
def getchangestest(w): # lex = korpuslex of avs
    import readvariant
    changeset  = readvariant.getvariant('lex_variation.txt')
    ccs = []                     # changeset = {900:[2,1]},{2:[900]} = (hv,v)
    (u,b,t) = gettav(w)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    # substitutions only
    for tav in tavs:
      if tav ==25937424601L: print 'found y'
      # get diff between tav and its translations
      subs = changeset.get(tav) or []
      if  12762815625L in subs: print 'found i'
      ch += map(lambda x: x-tav,subs)
#    for c in powerset(set(ch)):
#      addAll(lex.get(av+sum(c)),ccs)
    return [av+sum(c) for c in powerset(set(ch)) if av+sum(c)>0]

# TODO, give a value to the word pair depending on dl and how
# often the other one appears, as well as word length
# remove exact copies
def limit(w,ccset):
    props = []
    for (cc,n) in ccset:
      dist = dl.edit_dist(cc,w)
      if dist > lim:
        props.append((cc,n,dist))
        # TODO more snajs rules here
    return props
 











