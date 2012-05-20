# -*- coding: utf_8 -*-
from lexiconer import *
from xml.etree import ElementTree as etree
import tagtranslate
import glob
from xmlindent import indent

def validate(fil):
    entries,lexicon = readIt(fil) 
    lex             = lexicon.find('Lexicon')
#    lexdict         = mkLex(numbers=True,files=glob.glob('lexiconinfo/news/*xml'))#['kast.xml'])#files
    for i,entry in enumerate(entries):
      lemma = entry.find('Lemma')
      checkgram(lemma)  
      checkpos(lemma)

      # Splitting the entries
#      splitbypos(entry,lex,i)
    # start over to find all new entries form splitbypos
#    entries = lex.findall('LexicalEntry')
#    for entry in entries:
#      lemma = entry.find('Lemma')

      checklemgram(lemma)
      checkformrep(lemma)
      checkother(lemma)
      checksenseid(entry)
#      updateindex(lemma,entry,lexdict)
    indent(lex)
    open('testit2.xml','w').write(etree.tostring(lexicon,encoding='utf-8'))

def changeindex(fil):
    entries,lexicon = readIt(fil) 
    lex             = lexicon.find('Lexicon')
    lexdict = mkLex(numbers=True,files=glob.glob('lexiconinfo/news/*xml'))#['kast.xml']) #
    for entry in entries:
      updateindex(entry.find('Lemma'),lexdict)
    indent(lexicon)
    #print etree.tostring(lexicon)
    open('testit2.xml','w').write(etree.tostring(lexicon,encoding='utf-8'))

def move(fil):
    entries,lex = readIt(fil) 
    moving = ['gram','lemgram']
    for entry in entries:
      for moveobject in moving:
        form = getFormRepresentation(entry)
        if form is None:
          report(u'no formrep',getLem(entry))
        else:
          refs = getAttRef(form,moveobject)
          if refs!=[]:
            lems = getAtt(form,moveobject)
            lemma = entry.find('Lemma')
            for lem,_ in lems:
              lemma.insert(0,refs[0].makeelement(u'feat',{u'att':moveobject, u'val':lem}))
            for ref in refs:
              form.remove(ref)
    indent(lex)
    codecs.open('testL3.xml','w').write(etree.tostring(lex))
      
    
# TODO do we really want to concat all gram? 
def checkgram(lemma):
    grams = getAtt(lemma,'gram')
    news = ""
    gram = ""
    info = ""
    poss = []
    for (oldgram,gramr) in grams:
      gram = oldgram.strip(',()')
      newgram,pos = translate(gram)
      poss   += pos
      news   += newgram
      # if we change the gram and the old one consists of some letters we save the old one in 'inforamtion'
      if newgram!=gram and re.sub('[^\wÅÄÖÞÆåäöþæ]','',oldgram)!='':
        info += oldgram+' '
      lemma.remove(gramr)

    setpos = set(poss)
    setpos.discard('')
    for pos in setpos:
      # set the partOfSpeeach to contain this info
      lemma.insert(1,lemma.makeelement(u'feat',{u'att':'partOfSpeech', u'val':pos}))
      change('add pos-tag','',pos,lemma)

    if news.strip()!=gram.strip():
      change('gram',gram,news,lemma)
    if news.strip()!='':
      lemma.insert(1,lemma.makeelement(u'feat',{u'att':'gram', u'val':news}))
    if info!=news and info.strip()!='':
      index = indexofform(lemma)
      lemma.insert(index,lemma.makeelement(u'feat',{u'att':'information', u'val':info}))

def checkpos(lemma):
    poss = getAtt(lemma,u'partOfSpeech')
    if poss==[]:
      lpos,posref  = extractTag(getAtt(lemma,lemgram))
      if isOkPos(lpos):
        lemma.insert(1,posref.makeelement(u'feat',{u'att':'partOfSpeech', u'val':lpos}))

    for (pos,posref) in poss:
        if not isOkPos(pos):
          report(u'erronous pos: '+pos,lemma)

def splitbypos(entry,lex,index):
  # if there is more than 1 pos, copy this element and keep on pos in each
    lemma = entry.find('Lemma')
    poss = getAtt(lemma,'partOfSpeech')
    if len(poss)>1:
      report('splitting lemma into '+str(len(poss))+' entries',lemma)
      newentries = [clone(entry) for i in poss]
      for i,(pos,posref) in enumerate(poss):
        newentry = newentries[i]
        newlemma = newentry.find('Lemma')
        newposs = getAtt(newlemma,'partOfSpeech')
        for _,ref in newposs:
          newlemma.remove(ref)
        newlemma.insert(1,posref.makeelement(u'feat',{u'att':'partOfSpeech', u'val':pos}))
        # add new
        lex.insert(index+i,newentry)
      #remove orginal lemma
      lex.remove(entry)
         

def checklemgram(lemma):  
    lems = getAtt(lemma,'lemgram')
    poss = getAtt(lemma,'partOfSpeech')
    okchar = u'\w\d\.åäöþæ_'
    if len(lems)!=1:
      report(u'not 1 lemgram',lemma)
      print 'buu'
    else:
      lemgram,lemr = lems[0]
      newlem = cleanChars(okchar,lemgram,lemr,lemma)
      if len(poss)==1:
        pos,_ = poss[0]
        newlem = re.sub('\.\.\w{2,3}\.','..'+pos+'.',newlem)
        lemr.set('val',newlem)
        if newlem!=lemgram: change('lemgram',lemgram,newlem,lemma)
        if not set(lemgram).isdisjoint('?*()'):
          index = indexofform(lemma)
          lemma.insert(index,lemr.makeelement(u'feat',{u'att':'oldlemma', u'val':lemgram.strip(' ,.()')}))
      else:
      # report the number of postags, and set lemgram-tag to 'e'
        num = len(poss)
        report(u'bad pos, '+str(num),lemma)
        report(u'setting tag to e ',lemma)
        newlem = re.sub('\.\.\w{2,3}\.','..e.',newlem)
        lemr.set('val',newlem)
    #  report(u'setting tag to e due to several pos',lemma)
      
      # TODO add
      #l,xs = lookupLex(uselemgram)
      #if len(xs)>1:
      #   newlem = upgradelemgram(uselemgram) # upgrades index smartly
      #   change(uselemgram,newlem,lemma)     # report change
      #   lemr.set('val',newlem)

def checkother(lemma):
    xs = getAll(lemma,skip=['lemgram','partOfSpeech','gram','FormRepresentation'])
    if xs !=[]:
       report (u'too many elements in lemma',lemma)
    
def checkformrep(lemma):
    forms  = lemma.findall('FormRepresentation')
    for form in forms:
      writtens = getAtt(form,'writtenForm')
      okchar = u'\w\d\.åäöþæÅÄÖÞÆ '
      if len(writtens)>1:
        report (u'too many writtenforms in FormR',lemma)
      # TODO what if no written form?
      elif len(writtens)==1:
        written,writtenr = writtens[0]
        cleanChars(okchar,written,writtenr,lemma)


def checksenseid(entry):
    senses  = entry.findall('Sense')
    for sense in senses:
      if sense is not None:
        ids = sense.get('id')
        okchar = u'\w\d\.åäöþæÅÄÖÞÆ_'
        if re.search(u'^['+okchar+']+$',ids) is None:
          new = re.sub(u'[^'+okchar+']','',ids)
          change('sense cleanup',ids,new,entry.find('Lemma'))         # report change
          sense.set('id',new)
      
def updateindex(lemma,entry,lexdict):
    lems = getAtt(lemma,'lemgram')
    lemgram,lemr = lems[0]
    _,xs = lookupLex(lemgram,lexdict)
    def findindex(lem):
        _,xs = lookupLex(lem,lexdict)
        if xs>0:
          new,i = countindex(lem)
          if i>10: 
            print 'ooops to many'
            return '00'
          return findindex(new)
        else: return i,lem
    def countindex(lem):
        ind = re.findall('\.\.\w{1,3}\.(\d+)',lem)
        if ind==[]:
          print 'noo',lem
          return (lem,0)
        i = ind[0]
        return (re.sub(i,str(int(i)+1),lem),int(i))
    if xs>1:
      i,lem = findindex(lemgram)
      lemr.set('val',lem)
#      updateSense(i,entry)
      # update the dictionary, one less with name lemgram, one with name lem
      lexdict.update({lemgram : xs-1,lem:1})

# TODO should update them without overlapping others
#def updateSense(i,entry):

      

def cleanChars(okchar,string,ref,lemma):
    new = string
    if re.search(u'^['+okchar+']+$',string) is None:
      new = re.sub(u'[^'+okchar+']','',string).strip()
      change('cleanup',string,new,lemma)         # report change
      ref.set('val',new)
    return new
    
def report(string,lemma): # add this to some file
    lem,_ = getAtt(lemma,'lemgram')[0]
    codecs.open(reportfile,'a','utf8').write(string+' in '+lem+'\n')
reportfile = 'testrep'

# TODO allow 'med dat' etc in gram?
def translate(gram): 
    poss       = []
    newgram    = ""
    grams      = re.split('(?:och)|,',gram)
    # sort so that long tags are preferred to shorter ones (v. pass. rather than v.)
    gramdir = sorted(list(tagtranslate.easy.items()),key=lambda (item,x): (-len(item), item))
    for g in grams:
      found = False
      for pos,trans in gramdir:
        g = g.lstrip(' ,-')
        if g.startswith(pos):
          poss    += [trans.get('pos')]
          newgram += g[:len(pos)]+' '
          found = True
          break
      if not found: break 
    return (newgram,poss)

def isOkPos(pos):
    return pos in saldopos

def change(txt,old,new,lemma): # report old being set to new
    lem,_ = getAtt(lemma,'lemgram')[0]
    codecs.open(changefile,'a','UTF-8').write(txt+u' changed '+old+u' to '+new+u' in '+lem+u'\n')
changefile = 'changetest'

def updatelemgram(lemma):
    print 'i dont exist. mvh updatelemma'


saldopos = ['nn','av','vb','pm','ab','in','pp','nl','pn','sn','kn','al','ie'
           ,'mxc','sxc','abh','avh','nnm','nna','avm','ava','vbm','vba','pmm'
           ,'pma','abm','aba','pnm','inm','ppm','ppa','nlm','knm','snm','kna'
           ,'ssm']

def clone(elem):
    ret = elem.makeelement(elem.tag, elem.attrib)
    ret.text = elem.text
    for child in elem:
      ret.append(clone(child))
    return ret

def indexofform(lemma):
    j = 0
    for i,child in enumerate(lemma):
      if child.tag=='FormRepresentation':
         return i
         j = i
    return j


#kan vara i Formrepresentation -> flytta ut
# getLemma
# gram:   städa bort paranteser, komma punkter
#         översätt enligt tabell (tagTranslate)
#           sätt både gram, lemgramtag och information
# partOfSpeech: inSaldoSet
#                   report
#               lemgram ok: add as pos
#                   report 
# lemgram: inga konstiga tecken:
#                 ta bort, flytta till oldlemgram (oldForm)
#          ok tag: kolla i pos om det finns data
#                report
#          finns ingen annanstans:
#                ändra index enligt modell
#  annat (än information): report (move to wordform)
#  
#  Formrepresentation: writtenForm
#              inga konstiga tecken:
#                 städa bort de vanliga
#                 annars report
#                    
move(soederwall_supp)
validate('testL3.xml')