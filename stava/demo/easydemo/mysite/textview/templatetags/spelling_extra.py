# -*- coding: utf-8 -*-
from django import template
import re

register = template.Library()

@register.filter()
def second(x):
  #print 'second',x
  return x[1]

@register.filter()
def third(x):
  return x[2]

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
      #res += ' '.join([lex,':',entry['pos'],entry['hwtext']]) #,entry['gram']])
      res.append(entry['pos'])
    return ' '.join(set(res))


@register.filter()
def getsenses((w,lemgrams)):
 res = []
 for (l,lex,entry) in lemgrams:
   senses = entry['senses'].values() or '-'
   res.extend((lex,entry['pos'],s) for s in senses)

 print 'getsenses',w,lemgrams,l,lex,entry
 print 'res',res
 return res
   

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


#
#     {% autoescape off %}
#           {{ entry|formatentry }}
#         {% endautoescape %}
#
#        </li>
#    </ul>
#  {% endfor %}


#def formatxml(xml):
#  return xml
#  print 'ett'
#  a  = re.sub('<[A-Z][^>]*>' ,'<p>',xml)
#  print 'tva'
#  a  = re.sub('</[A-Z][^>]*>','</p>',a)
#  print 'tre'
#  gr = re.finditer('<feat\s*att="([^"]*)"\s*val="([^"]*)"\s*/>',a)
#  for g in gr:
#    print 'iter'
#    print 'a',a,'group',g.group()
#    print 'group1',g.group(1),'group2',g.group(2)
#    a = re.sub(g.group(),'<b>'+g.group(1)+'</b> '+g.group(2),a)
#    print 'done'
#  print 'finished'
#  return a
# 
#
#  
#def test():
# return formatxml('<Definition><feat att="partOfSpeech" val="nn" /></Definition>')
