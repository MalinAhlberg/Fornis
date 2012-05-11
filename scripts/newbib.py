# -*- coding: utf_8 -*-
import re

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

def gt(fil):
    lines = open(fil,'r').readlines() 
#    tag   = "(?:\d{1,3}\.*)*\s*[A-Z]\w{1,3}.\s\d{1,3}:.*"                 #gt
    tag = "(?:\d{1,3}\.*)*\s*((?:Ep|Ev|Högm)(\.))*\s*[A-Z]\w{1,3}.\s*\d{1,3}:.*"   #nt
#    tag = "(?:\d{1,3}\.*)*\s*(upp\.|uPp\.)\s*\d{1,3}:.*"   #nt2
    chap  = "\s*(\d*)\s*Kapitlet"
    txt   = ""
    for (n,line) in enumerate(lines):
      #line = line.decode().encode('utf-8')
      if re.match(chap,line):
         x = newChap(re.findall(chap,line)[0],n)
         txt += x
      else:
        c = re.search(tag,line)
        if c!=None:
          elem = mkTag('info',c.group()) 
          (st,end) = c.span()
          txt += line[:st]+elem+'\n'
        else: 
          txt += line
    #print txt
    open('utnt.xml','w').write(txt)

#
#
#    xs    = []
#    for (n,line) in enumerate(lines):
#        c = re.findall(tag,line)
#        if c!=[]:
#           xs += [str(n)+'\t'+'  '.join(c)]
#    open('whatsingt','w').write('\n'.join(xs))




def newChap(chap,n):
    begin = '<chapter name="'+chap+'">\n'
    if n==0:
       return begin 
    else:
       return '</chapter>\n'+begin

def mkTag(name,txt):
    return '<'+name+' name="'+re.sub('"','',txt)+'"/>'
    
           

gt('../nyabiblar/1917_bibeln-efs1927-nt.txt')
