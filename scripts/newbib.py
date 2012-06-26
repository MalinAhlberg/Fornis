# -*- coding: utf_8 -*-
import re
import codecs
from xml.etree import ElementTree as etree

def carl(fil):
    lines = open(fil,'r').readlines() 
    tag = "(\S{3}\s\d{1,3}):\d{1,3}"
    cap = ""
    txt = ""
    for (n,line) in enumerate(lines):
        b = re.match(tag,line)
        #print line
        if b is not None:
           c = re.findall(tag,line)[0]
           if cap != c:
              x    = newChap(c,n) # close last and append new tag
              txt += x
              cap  = c
           txt += re.sub(tag,mkTag('section',b.group()),line)
    open('ut.xml','w').write(txt)

# why does utf-8 take so much more time?
def gt(fil):
    lines = codecs.open(fil,'r').readlines() 
#    tag   = "(?:\d{1,3}\.*)*\s*[A-Z]\w{1,3}.\s\d{1,3}:.*"                 #gt
#    tag = "(?:\d{1,3}\.*)*\s*(upp\.|uPp\.)\s*\d{1,3}:.*"   #nt2
    txt   = ""
    for (n,line) in enumerate(lines):
      chap  = "\s*(\d*)\s*Kapitlet"
      line = re.sub('<poem.>','',line)  # ta bort poem
      if re.match(chap,line):
        x = newChap(re.findall(chap,line)[0],n)
        txt += x
      txt += extractdata((n,line))
    codecs.open('utnt3.xml','w').write(txt)

def extractdata((n,line)):
  print 'line',n
  def insertdata(match,elem,attr):
    if match!=None:
      print match.group(),line,match.span()
      elem = mkTag(elem,attr,match.group()) 
      (st,end) = match.span()
      print 'now have',line[:st]+elem+line[end:]+'\n'
      return line[:st]+elem+line[end:]+'\n'

  tag = u"(?:\d{1,3}\.*)*\s*((?:Ep|Ev|Högm)(\.))*\s*[A-Z][\wåäöæøÞß]{1,3}.\s*\d{1,3}:.*"   #nt
  added = insertdata(re.search(tag,line,re.U),'info','name')
  print line,added
  if not added:
    num = "\d+"
    # use match since the number should be in beginning of line
    added = insertdata(re.match(num,line),'part','name')
  return added or line


#tagtest = u"(?:\d{1,3}\.*)*\s*((?:Ep|Ev|Högm)(\.))*\s*[A-Z][\wåäöæøÞß]{1,3}.\s*\d{1,3}:.*"   #nt
#tagtest1 = u"[A-Z][\wåäöæøÞß]{1,3}.\s*\d{1,3}:.*"   #nt
#bokstaver = '[\wåäöæøÞß]'


def newChap(chap,n):
    begin = '<chapter name="'+chap+'">\n'
    if n==0:
       return begin 
    else:
       return '</chapter>\n'+begin

def mkTag(name,attr,txt):
    return '<'+name+' '+attr+'="'+re.sub('"','',txt)+'"/>'
    
           
#gt('../nyabiblar/1917_bibeln-efs1927-gt.txt')
gt('kast')

def test(fil):
    xmls = codecs.open(fil,'r').read()
    tree = etree.fromstring(xmls)
