# -*- coding: utf_8 -*-

from xml.etree import ElementTree as etree
                        # import qualified fast med exakt rätt namn,
                        # annars använd import Modul as nyttnamn

fil  =  "../filerX/Alexius.xml"

testxml = '''
          <doc>
          <para><inline font-size="12.00"
          font-style="Times"># 219 jak h&#xF6;rde aaf tinom wisdom och deylighet sakth,
          </inline></para>
          </doc>
            '''

prefix = "{http://rtf2xml.sourceforge.net/}"

def use(xmls):
    etree.register_namespace('',"http://rtf2xml.sourceforge.net/")
    tree = etree.fromstring(xmls)
    movePageNom(tree.find(prefix+'body'))
    return etree.tostring(tree)

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
              

utfilen = "kalas.xml"
open(utfilen,'w').write(use(open(fil).read()))
