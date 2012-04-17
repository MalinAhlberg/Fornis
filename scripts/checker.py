# -*- coding: utf_8 -*-
import re
import glob
import threading
from xml.etree import ElementTree as etree

# checks if the file contains the title elsewhere
def containsTitle(fil):
    print "start on",fil
    xml = open(fil,'r').read()
    etree.register_namespace('',"http://rtf2xml.sourceforge.net/")
    tree = etree.fromstring(xml)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information')
    tit1 = info.find(prefix+'title')
    tit = tit1.text
    text = findtext(tree.find(prefix+'body'))
    if not text.startswith(tit):
       print fil,"Title:",tit
       print "text",text[:20],"\n"
    print "finished",fil
    return fil

def findtext(tree):
    for e in tree:
        if e.text and e.text.strip():
           return e.text 
        elif findtext(e):
             return findtext(e)

def checkAll():
    for uri in files+filesNy:
        containsTitle(uri)
#        t = threading.Thread(target=containsTitle,args=(uri,))
#        t.start()

files   = glob.glob('../filerX/*.xml')
filesNy = glob.glob('../filerXNy/*.xml')

# TODO remeber to fix encoding when adding titles!
# for adding info to a list of xml files
# Each line of the input should contain first the filename
# and then a list of elements to add
# Eg. "file.xml year=2012 title=Rubriken" as input
def readAndAddInfo(uri):
   text = open(uri,'r').readlines()
   for uri in text:
        t = threading.Thread(target=addInfo,args=(uri,))
        t.start()

# add a new information to a file
# takes a line such as "file.xml year=2012 title=Rubriken" as input
# prints the new xml
def addInfo(line):
    xs = line.split()
    etree.register_namespace('',prefix)
    etree.register_namespace('','ns0')
    fil = open(xs[0],'r').read()
    tree = etree.fromstring(fil)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information')
    addTag(xs[1:],info)
    open('ny/'+xs[0],'w').write(tree)

# saves the info (a list of keys and values: ['key1=val1','key2=val2']
# to the tree. Updates the tags if the already exists, otherwise adds them
def addTag(info,tree):
    info = map(lambda x: x.split('='),info)
    for (tag,val) in info:
        tit = tree.find(prefix+tag)
        if tit is not None:
           tit.text = val
        else:
           new = etree.SubElement(tree,tag)
           new.text = val


prefix = "{http://rtf2xml.sourceforge.net/}"

def test2():
    return addInfo("../filerX/Nic-A.xml title=hej year=44")
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


