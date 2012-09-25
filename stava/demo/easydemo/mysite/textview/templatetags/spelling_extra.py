# -*- coding: utf-8 -*-
from django import template
import re
import HTMLParser

register = template.Library()

@register.filter()
def second(x):
  return x[1]

@register.filter()
def third(x):
  return x[2]

@register.filter()
def fourth(x):
  return x[3]


@register.filter()
def formatentry((w,lems)):
  lems = ([formatxml(l[1]) for l in lems])
  return '\n'.join(lems)

@register.filter()
def hits(w):
  if len(w)==1:
    return u'träff'
  else: return u'träffar'


@register.filter()
def firstline((w,lemgrams)):
    res = [] 
    for (lem,lex,entry) in lemgrams:
      res.append(entry.get('pos',''))
    return ' '.join(set(res))


@register.filter()
def getsenses((w,lemgrams)):
 res = []
 for (l,lex,entry) in lemgrams:
   senses = entry['senses'].values() or '-'
   res.extend((lex,entry['pos'],s,i) for i,s in enumerate(senses))
 return res
     
# TODO unused?
@register.filter()
def usetruncated(senses,morelist):
   return str(senses[3]) not in list(morelist)

@register.filter()
def dropwords(txt,n):
   wds = txt.split(' ')
   return wds[50:]

@register.filter()
def mklinks(txt):
  newtxt = ''
  for word in txt.split():
    bokstaver = u'åäöÅÄÖæÆøØÞþßÇàáçèéêëíîïóôûüÿᛘ∂' 
    normword = re.sub(u'[^\w'+bokstaver+']','',word).lower()
    linkword = ' <a  href="/onelex/'+normword+'">'+word+'</a>'
    newtxt += linkword
  return newtxt

   
@register.filter()
def addset(xs,x):
   return xs if x in xs else [x]+xs

@register.filter()
# TODO ugly function, unable to combine them otherwise
def addsetfourth(xs,x):
   i  = str(x[3])
   strxs = list(xs)
   return xs if i in strxs else i+xs

@register.filter()
# dont use, same as safe
def fromhtml(text):
   return HTMLParser.HTMLParser().unescape(text)


def getAtt(elem,val,none=[]):
    res = []
    if not elem is None:
      for feat in elem:
          value = feat.get('att')
          if value == val:
             res.append(feat.get('val'))
    if res:
      return res
    else:
      return none



