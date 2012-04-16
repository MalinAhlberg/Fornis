# -*- coding: utf_8 -*-

# kolla om title finns först i texten, skriv ut filnamn annars
# läsa in title och year från lista och lägga till i fil
# kolla om filnamnet finns med i en av sections-mapparna, skriv ut annars


import re
from xml.etree import ElementTree as etree

# checks if the file contains the title elsewhere
def containsTitle(fil,errs):
    xml = open(fil,'r').read()
    tree = etree.fromstring(xml)
    tit = tree.find(prefix+'title').text()
    text = findtext(tree.find(prefix+'body'))
    if not text.startswith(tit):
       print fil,"Title:",tit,"text",text[:20]
       errs += fil

def findtext(tree):
    for e in tree:
        if e.text and e.text.strip():
           return e.text 
        elif findtext(e):
             return findtext(e)

def test():
    return findtext(etree.fromstring(testxml))

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


