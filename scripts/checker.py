# -*- coding: utf_8 -*-
import re
import os
import glob
import threading
from xml.etree import ElementTree as etree
from usefuls import *


# add label tags, as specified in tagUri
# reads and writes to files in toDir
def addLabel(tagUri,toDir):
    print "reading labels from",tagUri
    files = open(tagUri,'r').readlines()
    tag = ""
    if files[0].startswith('#'):
       tag = files[0][1:].strip()
       print "will add tag",tag
       files = files[1:]
       for fil in files:
         if fil.strip():
           fil = fil.strip()
           path = os.path.join(toDir,fil+'.xml')
           print "adding tag to file",path
           xml = etree.fromstring(open(path,'r').read())
           doc = xml.find(prefix+'preamble').find(prefix+'doc-information')
           addTag(['label='+tag],doc)
           open(path,'w').write(etree.tostring(xml))
       

# for adding info to a list of xml files
# Each line of the input should contain first the filename
# and then a list of elements to add
# Eg. "file.xml | year=2012 | title=Rubriken" as input
def readAndAddInfo(uri):
   text  = open(uri,'r').readlines()
   toDir = os.path.join('..','titled')
   for line in text:
        addInfo(line,toDir)
   return toDir

# add a new information to a file
# takes a line such as "file.xml | year=2012 | title=Rubriken" as input
# prints the new xml
def addInfo(line,toDir):
    print "Info",line
    xs = line.split('|')
    xs = map(lambda x: x.strip(), xs)
    etree.register_namespace('',prefix)
    path = xs[0]
    if path.strip():
      fil  = open(os.path.join(filerX,path),'r').read()
      tree = etree.fromstring(fil)
      docinfo = tree.find(prefix+'preamble').find(prefix+'doc-information')
      addTag(xs[1:],docinfo)
      open(os.path.join(toDir,xs[0]),'w').write(etree.tostring(tree))

# saves the info (a list of keys and values: ['key1=val1','key2=val2']
# to the tree. Updates the tags if the already exists, otherwise adds them
def addTag(info,tree):
    info = map(lambda x: x.split('='),info)
    for (tag,val) in info:
        # if it is a year tag, split it into start and begin
        if tag=="year":
           # if the year is not an interval, use same start and end date
           if val.rfind('-')==-1:
              #print 'change val'
              val = val+'-'+val
           val = filter(lambda x: x!='"' and x!="'",val)
           #print 'year interval',val
           interval = val.split('-')
           info += [("begin",interval[0]),("end",interval[1])]
        # else add tag
        else: 
          tit = tree.find(prefix+tag)
          if tit is None:
             tit = etree.SubElement(tree,prefix+tag)
          tit.text = val.decode('utf-8')

def test2():
    return addInfo("Nic-A.xml | title=u\"hallå eller\" |  year=44","ny")
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
###############################################################################
# For checking the title, is repeated in the body text?
###############################################################################

def checkAll():
    for uri in allFiles
        containsTitle(uri)


# checks if the file contains the title elsewhere
def containsTitle(fil):
    xml = open(fil,'r').read()
    etree.register_namespace('',prefix)
    tree = etree.fromstring(xml)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information') # used to use findtext()
    tit1 = info.find(prefix+'title')
    tit = "" 
    if not tit1 is None: tit = tit1.text
    text = tree.find(prefix+'body').itertext()
    if not text.startswith(tit):
       print fil,"Title:",tit
       print "text",text[:20],"\n"
    return fil

#
#def findtext(tree):
#    alltxt = body.itertext()
#    for e in tree:
#        if e.text and e.text.strip():
#           return e.text 
#        elif findtext(e):
#             return findtext(e)

# prints the set titel and year
def hittaTitel(fil):
    print "start on",fil
    xml = open(fil,'r').read()
    etree.register_namespace('',prefix)
    tree = etree.fromstring(xml)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information')
    tit1 = info.find(prefix+'title')
    year = info.find(prefix+'year')
    tit = ""
    y   = ""
    if not tit1 is None: tit = tit1.text
    if not year is None : y = year.text
    return (fil,tit,y)


filerna1 = [glob.glob("../filerX/"+a+"*xml") for a in list('abcdefghijABCDEFGHIJ')]
def findthem():
    for lst in filerna1:
       for uri in lst:
        print hittaTitel(uri)


