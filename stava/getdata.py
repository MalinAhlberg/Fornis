from extracttxt import gettext,shownice,getLemgram,getWrittenforms
from normalize import norm
from xml.etree import ElementTree as etree
import codecs

def getdata():
    from readvariant import getvariant
    txt    = ' '.join(list(gettext('../filerX/Albinus.xml')))
    wds    = map(lambda x: norm(x).lower(),txt.split())
    d      = readlexnormal(['../scripts/lexiconinfo/newer/schlyter.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_main.xml'
                     ,'../scripts/lexiconinfo/newer/soederwall_supp.xml'])
    print 'will lookup each word'
    xs = map(lambda w: (w,d.get(w)),wds)

    codecs.open('results','w',encoding='utf8').write(shownice(xs))
 

def readlexnormal(files):
    d = {}
    for fil in files:
      s = open(fil,"r").read()
      lexicon = etree.fromstring(s)
      lex     = lexicon.find('Lexicon')
      entries = lex.findall('LexicalEntry')
      for entry in entries:
         lem = getLemgram(entry)
         forms  = getWrittenforms(entry)
         for form in forms:
           insertnormal(d,form,lem)
    return d

def insertnormal(d,form,lem):
    old = d.get(form)
    if old==None:
      lst = []
    else:
      lst = old
    d.update({form : [lem]+lst})

getdata()

