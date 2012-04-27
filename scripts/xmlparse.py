# -*- coding: utf_8 -*-

import re
from xml.etree import ElementTree as etree
from usefuls import *

fil  =  "../filerX/Alexius.xml"

testxml = '''
          <doc>
          <body>
          <para1><inline1 font-size="12.00"
          font-style="Times"># 219 jak h&#xF6;rde aaf tinom wisdom och deylighet sakth,
          </inline1></para1>
          <para2><inline2 font-size="12.00"
          font-style="Times"># 220 två
          </inline2></para2>
          <para3><inline3 font-size="12.00"
          font-style="Times"># 221 tre
          </inline3></para3>
          <para3><inline3 font-size="12.00"
          font-style="Times">221 tre
          </inline3></para3>
          </body>
          </doc>
            '''

# makes sure that a paraghraph is not interrupted by a pagebreak
def use(xmls):
    etree.register_namespace('',prefix)
    tree = etree.fromstring(xmls)
    concatTags(tree.find(prefix+'body'))
    return tree
    #return etree.tostring(tree)

# concatenates text in tags if they are interrupted by pagebreak
def concatTags2(tree,p = None):
# TODO do this on paras only
# do this before concatTags
    for elem in tree:
      # if the last tag is appendable and if this start with # ...
      if p!=None:
         p.text = p.text +' '+ elem.text 
         
      # if this is only a page numbering, move next text to it
      elif elem.text and isonlypagebreak(elem.text):
         p = elem

    return p


# concatenates text in tags if they are interrupted by pagebreak
def concatTags(tree,p = None):
# TODO do this on paras only
    pOld = p
    for elem in tree:
      # if the last tag is appendable and if this start with # ...
      if p!=None and elem.text and ispagebreak(elem.text):
         # then move text to last element and empty this
         p.text = p.text +' '+ elem.text 
         elem.text = ""
      # else, check whether this element is appendable
      elif elem.text and elem.text.strip():
         p = elem
      # then go through inner trees
      p1 = concatTags(elem,p)
      p = p1
    return p

def ispagebreak(text):
    stripped = text.strip()
    p1 = stripped[0:1]=='#'
    p2 = re.match(u'\[*\s*‡',stripped,re.U)
    return p1 or p2

# creates tags for pagenumbering in body
# maunal subsitution in xml. not safe, produces nested tags which are
# not accepted in standard xml
def tagPageN(tree):
    # we only want to change the body
    parts = re.split('<body>',tree,2)
    # and we want to close all page numbering-tags befor the body ends
    body = re.split('</body>',parts[1])
    # tag creation
    xml = tagPageNo(body[0])
    return parts[0]+'<body>'+xml+'</body>'+body[1]

# creates tags for pagenumbering
# maunal subsitution in xml. not safe, produces nested tags which are
# not accepted in standard xml
def tagPageNo(tree):
         i = 0 # position in string
         # inserts an element surrounded by text
         def insert(txt,pos,pos2,elem):
             return txt[:pos]+elem+txt[pos2:]

         # finds 'reg' in 'tree' (after position 'i') and inserts a tag 
         # of type 'typ' at the position of 'reg'
         def inserts(tree,typ,reg,i,close):
               newtree = tree
               while True:
                 m = re.search(reg,newtree[i:])
                 if m:
                    (st,end) = m.span()
                    num      = extractNo(m.group())
                    newelem = makeelem(typ,num,m.group()[:1],close)
                    newtree = insert(newtree,st+i,end+i,newelem)
                    close = True
                    i = i+end+len(newelem)
                 else: break
               return (newtree,close)

        # produces end tags if necessary
         def closeTag(tag,s,close):
             if close:
                return s+'</'+tag+'>'
             else: return s

         # insert tags for 'utgåvesidonummer'
         (t1,c)  = inserts(tree,"pagenum",re1,0,False)
         # end open tags
         t2      = closeTag("pagenum",t1,c)

         # insert tags for 'handskriftsidonummer'
         (t3,c1) = inserts(t2,"hskr",re2,0,False)
         # end open tags
         t4      = closeTag("hskr",t3,c1)
         return t4


# creates a tag, possibly after having closed earlier tag
# and reinserting end-brackets ('>')
def makeelem(tag,att,opt,close):
    x = closer = ''
    if opt=='>':
       x = '>'
    if close:
       closer = '</'+tag+'>'
    return x+closer+'<'+tag+' num=\"'+att+'\" >'

# extracts the pagenumber from a handskriftssidonummer and pagenumber
def extractNo(s):
    ok  = re.sub(hskTag,'',s)  
    return ''.join(filter(lambda x: x.isdigit() or x.isalpha(),ok))
    

             
# Tests
hskTag = r'(&#x2021;&#x2021;)|(&#8225;&#8225;)' 
utfilen = "kalas.xml"
#open(utfilen,'w').write(use(open(fil).read()))


def test():
    tree = etree.fromstring(testxml)
    _ = concatTags(tree.find('body'))
    print etree.tostring(tree)

def test2():
    tree = etree.fromstring(testxml)
    para = tree.find('body').find('para1').find('inline1')
    para.insert(1,tree.makeelement('num',{'p':'1'}))
    return etree.tostring(tree)
    #print etree.tostring(tree)

def makeelemm(tag,att,val):
    return '<'+tag+att+'='+val+'>'


