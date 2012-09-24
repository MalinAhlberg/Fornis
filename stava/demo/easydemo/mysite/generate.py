# -*- coding: utf-8 -*-
from xml.etree import ElementTree as etree
import codecs
import re
import os.path

# generatehtml :: textfile.xml -> website.html
# creates one link to variants for each word 
# and translate tags to html
def generatehtml(fil,variants,targetframe):
  xmls = codecs.open(fil,'r').read()
  body = etree.fromstring(xmls).find('body')
  for elem in list(body.iter()):
    if elem.tag=='para':
      elem.tag  = 'p'
      tags = tag(elem,variants,targetframe)
      elem.clear() # remove all text (including text inside other elements)
                   # this means we lose information about italics etc...
      elem.extend(tags)
  indent(body) 
  return etree.tostring(body)

# for testing
def generateandprint(infile,tofile,variants):
  open(tofile,'w').write(generatehtml(infile,variants,'dummyname'))

# adds one link to each word in elem
# word --> <a href="word-variant1-variant2">word</a>
def tag(elem,variants,targetframe):
  s = []
  text = ''.join(elem.itertext())
  for word in text.split():
    bokstaver = u'åäöÅÄÖæÆøØÞþßÇàáçèéêëíîïóôûüÿᛘ∂' 
    normword = re.sub(u'[^\w'+bokstaver+']','',word).lower()
    var = variants.get(normword,{})
    if var:
      linkword = elem.makeelement('a',{'href':mklink(normword,var)
                                      ,'target':targetframe})
    else:
      linkword = elem.makeelement('grey',{})
    linkword.text = word
    s.append(linkword)
       
  return s

def mklink(word,var):
  varlist = sorted([(d['dist'],w) for w,d in var.items()])
  return '/lexs/'+('-'.join([word]+[x[1] for x in varlist]))


### For parsing list of variants ###
""" parses variantlist on the form
      word:::distance1,edits1,variant1(in lex),lemma1a:lexiconname1a,lemma1b:lexiconname1b^^distance2...
      into
      {'word' : {'variant1': {'dist':n,'eds':m,lems:[lemmas]}}}
    or
      word:::variant1,distance1^^variant2,distance2^^...
      into
      {'word' : {'variant1': {'dist':n}}}
"""
def parsemap(fil):
  d = {}
  with codecs.open(fil,"r",encoding='utf-8') as f:
    for line in f:
      if line:
        wd,info = line.strip().split(':::')
        d[wd] = parseinfo(info)
  return d


def parseinfo(info):
  res = {}
  if info:
   for part in info.split('^^'):
     if part:
       xs = part.split(',')
       if len(xs)>3:
         res[xs[2]] = {'dist':int(xs[0]),'eds':int(xs[1])
                      ,'lems':map(lambda x: splitlems(x),xs[3:])
                      }
       else:
         res[xs[0]] = {'dist':float(xs[1]) }
  return res

def splitlems(x):
  return x.split(':')

# to make the html human-readable
def indent(elem, level=0):
    i = "\n" + level*" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

