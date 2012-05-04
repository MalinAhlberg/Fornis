# -*- coding: utf_8 -*-
import re
import os
from xml.etree import ElementTree as etree
from nltk.tokenize import PunktSentenceTokenizer
import cPickle as pickle

## OBS nyare version finns på kark!
# Segments text into sentences. Puts each sentence in an <s> xml elemnt
# Uses four modes to decide how the segmentation should be done:
# 'cap'   splits a sentence whenever a word is capitalized
# 'cpC'   splits after punctuation, comma or '¶' (unicode symbol),
#           if the following word is capitalized
# 'punkt' splits at punctuation, uses nltk
# 'para'  uses predefined paragraphs, does not split further
# 'cap' and 'cpC' ignores page numberings and roman numbers.


# for makefile. put segmentF and chunker in the directory, as well as sentenceinfo
#custom_common = sentence
#%.sentence: %.TEXT %.$(sentence_chunk)
#	python -m segmentF --element s --out $@ --text $(1) --chunk $(2) --segmenter $(sentence_segmenter) --model
# 

sentence_dir = '../sentenceinfo'

def grouptext(txt,mode,segmenter=None):
    return groupbyreg(txt,regex(mode),mode,segmenter)

# reads files in sentence_dir and adds the correct encoding
def findmode(fil):
    fil,ext = os.path.splitext(os.path.basename(fil))
    print 'find file',fil
    def findFile(path):
      txt = open(path,'r').readlines()
      isInFile = False
      for line in txt:
          splitted = line.split()
          if splitted:
            (file2,ext2) = os.path.splitext(os.path.basename(splitted[0]))
            if file2 == fil:
             isInFile = True
      return isInFile

    if findFile(os.path.join(sentence_dir,'dot.txt')):
      return 'punkt'
    elif findFile(os.path.join(sentence_dir,'dotComma.txt')):
      return 'cpC'
    elif findFile(os.path.join(sentence_dir,'paras.txt')):
      return 'para'
    elif findFile(os.path.join(sentence_dir,'capital.txt')):
      return 'cap'
    else:
      return 'punkt'

def span_tokenize(text,mode,segmenter=None):
    """
    Given a text, returns a list of the (start, end) spans of sentences
    in the text.
    """
    if mode=='punkt':
      lst = segmenter.span_tokenize(text)
    else:
      slices = grouptext(text,mode,segmenter)
      i  = 0
      #i0 = 0
      lst = []
      for sl in slices:
        if len(sl)!=0:
          from itertools import takewhile
          ws = list(takewhile(lambda x: x in '\n\r\t\f\v ',sl))
          j = len(sl)-1 +i+ (1 if i==0 else 0)
          i = i+(len(ws)-1 if len(ws)> 0 else 0)
          lst += [(i,j)]
          i = j+1


          #j = i+len(' '+sl.lstrip())-1
          #nxt = i+len(sl)-1
          #lst += [(i0,j)]
          #i   = nxt+1
          #i0  = i
    return lst


# returs appropiate regex for the modes
def regex(mode):
    if mode == 'cap':
       return cap
    if mode == 'cpC':
       return cpC
    if mode == 'para':
       return ''
    else:
       return ''  #punkt


def groupbyreg(txt,reg,mode,segmenter): 
      if mode=='punkt':
        return segment(txt,segmenter)

      if mode=='para':   # segmented by paragraphs, do not segment further
        return [txt] 

      else:
        chunks = []
        nxtchunk  = '' 
        def breakIt(match,nxtchunk,txt,chunks,mode):
           (st,end)    = match.span()
           (first,sec) = extractStartAndStop(match.group(),mode)
           chunk       = nxtchunk+txt[:st]+first
           chunks      += [chunk]
           nxtchunk    = sec
           txt         = txt[end:]
           return (nxtchunk,txt)
 
        while True:
          # look for § 1. 
          n = re.search(parastring,txt,flags=re.UNICODE)
          # if we find it, split here
          if n:
            (nxtchunk,txt) = breakIt(n,nxtchunk,txt,chunks,'cap')
          # else look for our normal sentence splitter
          else:
            m = re.search(reg,txt,flags=re.UNICODE)
            if m:
              (st,end)    = m.span()
              # roman numbers etc. can be ignored
              if not ignore(m.group(),mode):
                (nxtchunk,txt) = breakIt(m,nxtchunk,txt,chunks,mode)
              else: 
               nxtchunk = nxtchunk+ txt[:end]
               txt = txt[end:]
            else: 
               chunks += [nxtchunk+txt]
               break

        return chunks 

# defines which part of the stop-section that belong to the new vs. old sentence
# nltk span should not use the sentence counter. our should use it in some way?
def extractStartAndStop(s,x):
    if x=='cap':
#       n = re.search(uppers,s,flags=re.UNICODE)
#       (st,e) = n.span()
#       return (s[:e-1],s[e-1:])
       return ('',s)
    else: #if x=='cpC':
       n = re.match(onlypunkt,s,flags=re.UNICODE)
       if n:   ## OBS change here to new
          (st,e) = n.span()
          return (s[:e],s[e:])
          #return (s[:-1],s[-1:])

# if roman number, don't count as capitalized
def ignore(string,mode):
    hasRoman = ()
    if mode=='cpC':
      punktRoman = punkt+u'('+pagenumbers+'u)*\s*'+romanpattern+'\s*$'
      hasRoman   = re.match(punktRoman,string,flags=re.U | re.I)
    if mode=='cap':
       hasRoman = re.match(startstring+romanpattern+'$',string,flags=re.U | re.I)
    return hasRoman is not None
    
    

################################################################################
# Regular expressions
################################################################################

# upper case letters
uppers = u"[ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖÞÆ]"

p1 = u'[\s>]#\s*[0-9]+'
p2 = u'\[\s*‡‡\s*[0-9]+\s*[abrv]*\s*\]'
p3 =      u'‡‡\s*[0-9]+[abrv]*'
pagenumbers = p1+'|'+p2+'|'+p3 

startstring = u'(^|\s)'
onlypunkt   = u'[.,¶]'
punkt       = u"[.,¶]\s*" 
parastring  = u'§\.*\s*[0-9]+\.*' # §. 1. 

cap = startstring+'\s*'+uppers+'\w*'
cpC = punkt+u'('+pagenumbers+u')*\s+'+uppers+'\w*'

# roman numbers, may use j instead of i. 
romanpattern = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})([IJ]X|[IV|V?[IJ]{0,3})'

#############################################################################
# For normal sentences, use nltk
#############################################################################

def segment(txt,segmenter):
    return segmenter.tokenize(txt)


txt = u"""[79] Ther epter wille konung Eric aff Danmark
och hertog Magnus göra en fast frijdh och wenskap sich emellen, ther
fore kommo the til hopa widh landamäret, med stoort pråål
på bådha sidhor, och wardt itt stoort hoff hollet, och
öffuades mong riddarspeel med stäkande och bräkande, Och
bliffuo både förstarne wel foreente, så at hertogen skulle
giffua konung Eric fyra tusende löduga mark silff, Colneska wicht, Thet
war först sex tusende, så bleeff thet fyra tusend, och på thet
sidzsta bleeff thet icke meer än tw tusende löduga mark silff, som
betalas skulle, ty hertogen talade på stoor skadhageld, ther före
wordo fyra tusende aff slaghet, Och skulle konung Eric haffua
Lödöse slott i pant så lenge han skulle få silffret, och
en Swensk riddere som heet her Swantopolk skulle haffua slottet inne och
giffua konung Eric hundrade löduga mark silff hwart åår,
så lenge all summan betaladt wardt,  Och konung Eric lagde sich thå
ther emellen at hertogen och konung Waldemar skulle warda forlijkte, Ty at
konung Waldemar achtade bliffua i Danmark och ther hade han Malmö och
Träleborg som han hade fååt i brudhaskatt med drottning
Sophia, och epter thet at samma Sophia nw war dödh, begerede han intit
regemente, vtan aleenast sitt arffua godz, och toogh han sich ena hustru i
Danmark som heet Chirstina, och när hon dödh war, fick han
greffuans dotter aff Getzskogh, som heet Katherina, Och noghot ther epter at
konung Eric hade förlijkt bådha brödherna, kom konung Waldemar
til Askanääs, ther vplätt han sinom brodher hertog Magnuse ey
aleenast then halff part aff rijkit som honom tilsagder war, vtan och all
then rett som han hade til heela rijkit, och gaff honom ther vppå sitt
breff i rikesens rådz närwaru, Och giorde han samma vplätning
aff en frij wilia onödd, och otwingat, och forplichtade han sich widh
ban til at aldrig wilia saka ther vppå, Och skal man weta i then tijdhen
och noghot tilförenne, pläghade the som noghro contracter eller
stoor forplichtelse giorde, giffua noghro biscopar befalning at banlysa sich
om the icke höllo thet the loffuade, Så giorde och nw konung
Waldemar, och än thå, at han så wedhersade rikit, wille doch
hertog Magnus icke gerna taga sich konungs nampn vppå, Men epter thet at
rikesens rådh [80] wåro thet så högeliga aff honom
begierende, giorde han thet, Ty at thet wart föregiffuit at hans brodher
war för sitt löszachtiga liffuerne och ostadughet skuld, icke
skickeligen til, at bliffua i regementet, Gåffuo och rikesens rådh
theres breff ther vppå, at konung Waldemaar läät sinom brodher
rikit frijt vpp, Samma vplåtning i Askanääs skedde epter
Christi byrdh tolffhundrade och niyo och siwtiyo åår, och sedhan
widh Mora steen wedersade han rikit, och hertogen bleeff thå hyllat
för konung, och Crönter i Vpsala, Ena reeso stadhfeste konung
Waldemar samma vplåtning i Skeninge och än thå at han
[så] offta vpsade rikit, så stoodh han doch hwarken widh ordh eller
eedhar, vtan [offta] vpwekte obestond emoot konung Magnus, och wordo the jw
åter forlikte, Ordh och ära är en herres eller förstes
yppersta Clenodium, thet honom stoorligha böör at forwara, Och
än thå at ostadugheet, och icke bliffua widh ordh och sanning,
är en sådana odygd, at hon alle stedes straffandes är, Så
är hon doch aldra mest straffandes, om hon finnes bland herrar och
förstar, ty at konunga ordh reknas högt, ther fore skola the och
wara san, och then ther högt är besetin, han warder aff mongom
beskodat och beseedder, ty skal han och ärliga skicka sich, annars
bliffuer han aff hwar man forachtat, som med thenna konung Waldemar skeedt
är, och jw högre en är besetin, jw större bliffuer hans
fall,"""

txt2 = u"""Gudh som all ting haffuer skapat menniskione til
godho och gagn, han haffuer thet ock aff sinne ewiga godheet och försyyn
så förordinerat och skickat, at theres liffuerne och regemente som
fordom dags i werldenne leffuat haffua bescriffuas skulle, theres
epterkommandom til en rettilse och warnagel, aff huilkom the lära motte,
hwad anslag lyckosameliga tilgå pläga, och hwad som plägar
illa bekomma och lyktas med en oond affgong, Så at epterkommarene mogha
lära aff theras förfäders welferdh eller forderff, huru the
sich i all stycke skicka skola, och hwad nyttoght eller skadeligit wara
pläghar. Ja epterkommarene haffua och ther en stoor fordeel aff, Ty thet
är jw betre bliffua wijs aff en annars ofärdh än aff sin
eeghen, Och böör historier eller Cröneker så scriffna
wara, at the föregiffua, så mykit som mögeliget kan wara, alla
vmstendigheeter, aff hwad oorsack och tilfelle, obestond örlig och
krijgh kommit är, och huru fridh och roligheet bewarat warder, ty the
kunna thå med frucht läsna warda, och äro them som epterkomma,
såsom en spegel, ther the mogha see vthinnan, hwad som bestond eller
obestond med sich haffuer, hwar vthaff land och stedher wexa til, eller huru
the förlagda warda.    Thet är icke noogh at man weet huru örlig
och krijgh haffuer tijdt och offta warit i werldenne Man behöffuer och
at weta aff hwad orsack sådana kommit är, Ja, så pläghar
jw mäst wara, at the komma på obestånd som sielffue giffua
ther tilfelle til, Och the vndtwijka obestond som tilfellen vndtwijka kunna,
Ther före är thet nyttogt, at man weet huru örligh <och>
krijgh kan [2] förtaghet och förekomit warda Såå är
ey heller noogh at man weett huru froma förstar vnderstundom haffua
warit i verldenne, the ther fridh och rooligheet hållet haffua, vtan man
och weett hwad sätt the ther til hafft haffue, huilkit Cröneke
scriffuaren föregiffua skal, them til epterdöme som
epterkomma."""

txt3 = """Miserunt iudei ierosolymis &c Judhane sändhe aff ierusalem preste ok kläreka at spöria sanctum iohannem sigiande hwat es tu Han vidhirgik sannindena ok nekadhe ey vtan sagde, ey är iak christus The sagdho huat est thu tha, äst thu helias som koma scal for domadagh, han sagdhe ey är helie persona min persona The sagdho äst thu propheta, han sagdhe ey är iak then propheta som scriptin sighir aff at gudh bödh allom lydha hulkin christum tekna  The sagdho huat äst thu tha, at vi maghom gifua wis swar them som oss sände Huat sighir thu aff tik siälfuom, han sagdhe iak är ropande röst j ödhknenne bidhiande at redha  vars herra vägh Swa som ysaias propheta sighir The sagdhe hwi döpir thy vm thu är ey christus ok ey helias Han suaradhe oc sagdhe Jak döpir j vatne än ihesus christus hulkin som stodh midhuaghu mällan idhir, Hulkin j ey visten vara sannan gudh ok sannan man han är then som koma skal ok predica eptir mik, hulkin förra var är iak var thy at han är min skapare, hulkins skotwängia iach är ey värdoghir at lösa han skal döpa idhir j thes helgha anda makt"""
txt4 = "XXVI. Kirkyugarther skal ee gilder uæra. bathe uinter ok sommar. kirkyugarﬂ skal skipta bola mællum. oc bool slict sum annat Ligger kirkyugarﬂer alder open. thæt ær thrigia marka sak. ligger halfuer open thæt ær tolföra sak. ligger thrithiunger öpen thæt ær siæx öra sak. thætta a biscuper. æn sithan a hæræth fore bolka huar .VIII. örtogher"
