# -*- coding: utf_8 -*-
import re
import usefuls
from xml.etree import ElementTree as etree

# encoding? must be ok for getting last controll right
# check that there is no other tag?

def extractText(fil):
    inp  = open(fil,'r').read() 
    xml  = etree.fromstring(inp)
    txt  = ''
    def addText(elem,txt):
        if not elem.text is None:
          txt += elem.text 
    body = xml.find(usefuls.prefix+'body')
    alltxt = body.itertext()
    for t in alltxt:
       txt += ' '+t 
    # addText(body,txt)
    # #sections = body.findall(usefuls.prefix+'section')
    # paras    = body.iterfind(usefuls.prefix+'para')
    # for p in paras:
    #   addText(p,txt)
    #   p.findall(usefuls.prefix+'inline')
    return txt 

def countSentence(txt,punkt):
    if len(punkt)==1:
       ss  = txt.split(punkt)
    else:
       ss  = splitBy(txt,punkt)
    whiteSpace = "\n\r\f\t\v"
    boundaries = whiteSpace+",.:;?!"
    for s in boundaries:
       ss = map(lambda t: t.replace(s,' '),ss)
    lens   = []
    uppers = []
    for sent in ss:
      sent = removePageN(sent)
      if bool(sent.strip()):
        lens   += [len(sent.split())]
        uppers += [sent.strip()[0].isupper()]
    return lens,uppers


def removePageN(sent):
    m  = re.search(usefuls.re1,sent)
    if not m is None:
       sent = sent[:m.start()]+sent[m.start():]
    m2 = re.search(usefuls.re2,sent)
    if not m2 is None:
       sent = sent[:m.start()]+sent[m.start():]
    return sent

# TODO START Fara gets None here why?
def rankText(fil):
    txt = extractText(fil)
#   print txt[:80]+txt[-20:]
#   txt = fil
    def mediumLen(xs):
        return reduce(lambda x, y: x+y,xs)/float(len(xs))
    def okLength(x):
        return x>9 and x<31
    lens,caps = countSentence(txt,'.')
    rank1 = []
    mlen = mediumLen(lens)
    mediumCap = len(filter(lambda x: x, caps))/float(len(caps))
    res = {'rank' : 1,'Pleng' : mlen, 'caps' : mediumCap, 'file' : fil}
    if okLength(mlen):
        return res
    
    (klen,caps) = countSentence(txt,',')
    mklen = mediumLen(klen)
    if okLength(mklen):
        mediumCap = len(filter(lambda x: x, caps))/float(len(caps))
        res.update({'rank' : 2,'Cleng' : mklen, 'caps' : mediumCap, 'file' : fil})
        return res

    (xlen,_) = countSentence(txt,uppers)
    mxlen = mediumLen(xlen)
    if okLength(mxlen):
       res.update({'rank' : 3, 'Uleng' : mxlen})
       return res

    return res.update({'rank':4})

          
uppers = u"ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖ"
def splitBy(txt,stoppers):
    parts = []
    j = 0 
    for (i,c) in enumerate(txt):
        if c in stoppers:
           parts += [txt[j:i]]
           j = i
    parts += [txt[j:]]
    return parts
           

def rankAll():
    ranks = []
    for fil in ["../filerX/Fara.xml"]: #usefuls.allFiles:
       print "fil",fil
       res = rankText(fil)
       ranks += [res]
       if res is None:
          print "Woo",res
    printres(ranks)

def printres(res):
   best = good = ok = bad = ''
   res.sort()
   s = ""
   print res
   for b in res:
     fil   = b.get('file')
     pLeng = str(b.get('Pleng'))
     caps  = str(b.get('caps'))
     if b.get('rank')==1:
            best += fil+'\t'+pLeng+'\t'+caps
     elif b.get('rank')==2:
        good += fil+'\t'+str(b.get('Cleng'))+'\t'+caps+'\t'+pLeng
     else:
        s = file+'\t'+str(b.get('Uleng'))+'\t'+caps+'\t' +pLeng+'\t'+b.get('Cleng')
        if b.get('rank')==3:
            ok += s
        else:
          bad += s
   
   open('best.txt','w').write(best)
   open('good.txt','w').write(good)
   open('ok.txt'  ,'w').write(ok)
   open('bad.txt' ,'w').write(bad)


