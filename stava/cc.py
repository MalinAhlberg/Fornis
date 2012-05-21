# -*- coding: utf_8 -*-
from normalize import iso,hashiso

#TAV: för ett ord, antistrip, kolla av, räkna ut av:t för varje bi- och ev. trigram.
#        spara. = alfabet
#få cc = variationer:
#             transpositions -automatiskt
#             deletions      - gå igenom alfabetet och kolla ordet plus varje aav(bokstavish)
#             insertions - gå ingenom tav:en och kolla ordet-minus varje tav
#             substitute - gå igenom både tav och aav och lägg till varje aav och ta bort ett tav
#

# finds the 'aav' alphabet, consisting of all strings, bigram and trigrams
def alphabet(wds):
    a =set([])
    for w in wds:
      u,b,t = gettav(w)
      map(lambda x: a.add(x),u+b+t)
    return a

# gets the av:s for a string
def gettav(w,keep=False):
    sw = '^'+w+'$' if keep else '_'+w+'_'
    #unis,bis,tris = [[],[],[]]
    #unis = [hashiso(w)]
    unis = [iso(w[i]) for i in range(len(w))]
    #for i in range(len(w)+1):
    #  bis += [iso(sw[i])+iso(sw[i+1])]
    bis = [iso(sw[i])+iso(sw[i+1]) for i in range(len(w)+1)]
    tris = []
    if len(w)>5:
#      for i in range(len(w)-1):
#        tris += [iso(sw[i])+iso(sw[i+1])+iso(sw[i+2])]
      tris =  [iso(sw[i])+iso(sw[i+1])+iso(sw[i+2]) for i in range(len(w))]
    return unis,bis,tris

# gets character confusion, the set of words comparable to this one
# how deep should we go? just one del/sub or insertion?
def getccs((w,av),lex,alphabet,ccs=[]): # lex = korpuslex of avs
    xs = lex.get(av) #transpositions
    addAll(xs,ccs)
    (u,b,t) = gettav(w)
    tavs = u+b+t
    # deletions
    for aav in alphabet:
      addAll(lex.get(av+aav),ccs)
      # substitutions
      for tav in tavs:
        addAll(lex.get(av+aav-tav),ccs)
    # insertions
    [addAll(lex.get(av-tav),ccs) for tav in tavs]
#    for tav in tavs:
#      addAll(lex.get(av-tav),ccs)
    return ccs # groupandcount(ccs)
    
def addAll(res,ccs):
    if res!=None:
      ccs += res.items() #keys()

def groupandcount(ccs):
    ccs.sort()
    return itertools.imap(lambda (x,y): (x,len(list(y))),itertools.groupby(ccs))


       
def getchanges(w,lex,changeset): # lex = korpuslex of avs
    ccs = []                     # changeset = {900:[2,1]},{2:[900]} = (hv,v)
    (u,b,t) = gettav(w,keep=True)
    av   = sum(u)
    tavs = u+b+t
    ch   = []
    # substitutions only
    for tav in tavs:
      # get diff between tav and its translations
      subs = changeset.get(tav) or []
      ch += map(lambda x: x-tav,subs)
    [addAll(lex.get(av+sum(c)),ccs) for c in powerset(set(ch)) if av+sum(c)>0]
    return ccs

def powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])

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
 
