# -*- coding: utf_8 -*-

import re
from xml.etree import ElementTree as etree
                        # import qualified fast med exakt rätt namn,
                        # annars använd import Modul as nyttnamn

fil  =  "../filerX/Alexius.xml"

testxml = '''
          <doc>
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
          </doc>
            '''

prefix = "{http://rtf2xml.sourceforge.net/}"

def use(xmls):
    etree.register_namespace('',"http://rtf2xml.sourceforge.net/")
    tree = etree.fromstring(xmls)
    (new,_) = concatTags(tree)
    #movePageNom(tree.find(prefix+'body'))
    return etree.tostring(new)

val = None
def movePageNom(tree):
    global val
    #print tree.tag
    def choose(n,m):
        if n: return n
        else: return m
    for elem in tree:
        n = pageN(elem)
        movePageNom(elem)
        m = val
        p = choose(n,m)
        #print "now val is",p
        if p:
           if elem.tag ==prefix+"para":
              #print "in para", elem.tag
              elem.set("pagenumber",p)
              val = None
           else:
              #print "in tag",elem.tag,"setting var to",p
              val = p

def test():
    (t,_) = concatTags(etree.fromstring(testxml))
    print etree.tostring(t)

def concatTags(tree,p = None):
    pOld = p
    for elem in tree:
      # if the last tag is appendable and if this start with # ..
      # obs flytta ej text uppåt!!
      if p!=None and elem.text and elem.text.strip()[0:1]=='#':
         # then move text to last element and empty this
         p.text = p.text +' '+ elem.text 
         elem.text = ""
      # else, check whether this element is appendable
      elif elem.text and elem.text.strip():
         p = elem
      # then go through inner trees
      (_,p1) = concatTags(elem,p)
      p = p1
    return (tree,p)


rex2 = re.compile(r"""(\[\s*&\#x2021;&\#x2021;\s*[0-9]*[abrv]*\s*\])|(&\#x2021;&\#x2021;\s*[0-9]*[abrv])|
                      (\[\s*&\#8225;&\#8225;\s*[0-9]*[abrv]*\s*\]) |(&\#8225;&\#8225;\s*[0-9]*[abrv])""",re.X)
def tagPageNo(tree):
         re1 = r'[ >]#\s*[0-9]*'
         re2 = re.compile(r"""(\[\s*&\#x2021;&\#x2021;\s*[0-9]*[abrv]*\s*\])|(&\#x2021;&\#x2021;\s*[0-9]*[abrv])|
                      (\[\s*&\#8225;&\#8225;\s*[0-9]*[abrv]*\s*\]) |(&\#8225;&\#8225;\s*[0-9]*[abrv])""",re.X)
         i = 0
         intag = "<>"
         def insert(txt,pos,pos2,elem):
             return txt[:pos]+elem+txt[pos2:]
         def inserts(tree,typ,reg,i):
               newtree = tree
               while True:
                 m = re.search(reg,newtree[i:])
                 if m:
                    (st,end) = m.span()
                    num      = extractNo(m.group())
                    newelem = makeelem(typ,num,m.group()[:1])
                    newtree = insert(newtree,st+i,end+i,newelem)
                    i = i+end+len(newelem)
                 else: break
               return newtree

         t1 = inserts(tree,"pagenum",re1,0)
         t2 = inserts(t1,"hskrpagenum",re2,0)
         return t2


def makeelem(tag,att,opt):
    if opt=='>':
       x = '>'
    else: x = ''
    return x+'<num '+tag+'=\"'+att+'\" />'

def extractNo(s):
    ok  = re.sub(hskTag,'',s)  
    return ''.join(filter(lambda x: x.isdigit() or x.isalpha(),ok))
    

def pageN(elem):
    if elem.text:
       t = elem.text.strip()
       x = None
       if t.startswith('#'):
          t = t[1:].strip()
          x = ''
          i = 0
          while i<len(t) and t[i].isdigit():
                #print "och nu",t[i]
                x = x + t[i]
                i = i+1
          elem.text = t[i:]
       return x
    else: return None
              
# TODO
#tag1 = r'[ >]#\s*[0-9]*'
##innertag2 = ""
#innertag2 = re.compile("""(&\#x2021;&\#x2021;|&\#8225;&\#8225;)  # the alternative '#'-sign
#                           \s*[0-9]*[abrv]*                       # the page number""",re.X)
#tag2 = re.compile(r'(\[\s*'+innertag2+'\s*\])|'+innertag2)

hskTag = r'(&#x2021;&#x2021;)|(&#8225;&#8225;)' 
utfilen = "kalas.xml"
#open(utfilen,'w').write(use(open(fil).read()))
