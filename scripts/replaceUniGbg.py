# -*- coding: utf_8 -*-
import codecs
import re
"""
Script for transforming the 'Förabeten till 1734 års lag'-txt files to xml
while inserting the typographic information as xml annotations
"""
def mkUniGbg(fil,n,utfil):
  ss = codecs.open(fil,'r',encoding='utf-8').read()
  subs = [('\r','')
         ,(r'([^\d])/(.*?)/([^\d])',r'\1 ITALIC \2 ITALIC \3')
         ,(r'<(.*?)>',r'<footnote> \1 </footnote>')
         ,(r'<([^>]*?)$',r'<marginal> \1 </marginal>')
         ,(r'&lt;(.*)&gt;',r'<footnote> \1 </footnote>')
         ,(r'&lt;([^>\n]*)$',r'<marginal> \1 </marginal>')
         ,(r' ITALIC (.*?) ITALIC ',r'<italic>\1</italic>')
         ,(r'^\s*#(\S*)',r'<pg num="\1"/>')
         ,(r'^\s*-(.*)$',r'<centeredheadline>\1</centeredheadline>')
         ,(r'\*(.*?)\*',r'<bold>\1</bold>')
         ,(r'_(.*?)_',r'<emphasis>\1</emphasis>')
         ,(r'\|(.*?)\|',r'<smallcaps>\1</smallcaps>')
         ,('&','&amp;')
         ,(r'^\t',r'</para><para>\t')
         ,(r'(\S*)-\s*\n((s*<.*?>.*\n)*)([^\s<]*)',r'\1\4 <wordbreak break="\1-\4"/> \2')
         ]
         # the & in the last group of wordbreak prevents footnote tags to become part of word
         # the extra spaces in footnotes and marginal is needed to get correct tokenization
  head = u"""<article>\n<head>\n<title>1734 års lag Förarbeten vol %s</title>
            <date>1734</date>
            </article>
            </head>\n\t<para>""" % n
  end  = '</para>\n\t</article>'
  codecs.open(utfil,'w',encoding='utf-8').write(head+multisub(subs,ss)+end)

def multisub(subs,s):
  #print 'subs',subs
  for (expr,sub) in subs:
    print 'e:',expr
    print 's:',sub
  #  print 'type',type(s)
    s = re.sub(expr,sub,s,flags=re.M)
  return s

def replace():
  import glob
  for txtfile in glob.glob('unconverted/foerarbete*txt'):
    name    = txtfile.split('.')[0]
    xmlfile = name+'.xml'
    number  = name.split('_')[-1]
    print 'converting',txtfile,'to',xmlfile
    mkUniGbg(txtfile,number,xmlfile)
