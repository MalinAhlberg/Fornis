# -*- coding: utf_8 -*-
import re
import os
import glob
import threading
from xml.etree import ElementTree as etree

# TODO what will happen to ns0 usw when reading file many times?
# OK kolla om titel stämmer
# Test   lägga till tag om innehåll
# OK lägga till år och namn med rätt encoding och antal fnuttar, add begin end
# OK do not care about new lines


# adding label-tag, should read section/*
# (not tested)
def addLabel(tagUri,toDir):
    files = open(fil,'r').readlines()
    tag = ""
    if files[0].startswith('#'):
       tag = files[0][1:].strip()
       files = files[1:]
    for fil in files:
       xml = etree.fromstring(open(fil,'r').read())
       doc = tree.find(prefix+'preamble').find(prefix+'doc-information')
       addTag(['label='+tag],doc)
       open(os.path.join(toDir,fil)).write(etree.toString(xml)
       

    
# checks if the file contains the title elsewhere
def containsTitle(fil):
    xml = open(fil,'r').read()
    etree.register_namespace('',prefix)
    tree = etree.fromstring(xml)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information')
    tit1 = info.find(prefix+'title')
    tit = "" 
    if not tit1 is None: tit = tit1.text
    text = findtext(tree.find(prefix+'body'))
    if not text.startswith(tit):
       print fil,"Title:",tit
       print "text",text[:20],"\n"
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

# for adding info to a list of xml files
# Each line of the input should contain first the filename
# and then a list of elements to add
# Eg. "file.xml | year=2012 | title=Rubriken" as input
def readAndAddInfo(uri):
   text  = open(uri,'r').readlines()
   toDir = os.path.join('..','titled')
   for uri in text:
        t = threading.Thread(target=addInfo,args=(uri,toDir))
        t.start()
   return toDir

# add a new information to a file
# takes a line such as "file.xml | year=2012 | title=Rubriken" as input
# prints the new xml
def addInfo(line,toDir):
    xs = line.split('|')
    xs = map(lambda x: x.strip(), xs)
    etree.register_namespace('',prefix)
    fil = open(os.path.join(filerX,xs[0]),'r').read()
    tree = etree.fromstring(fil)
    info = tree.find(prefix+'preamble').find(prefix+'doc-information')
    addTag(xs[1:],info)
    print etree.tostring(info)
    open(os.path.join(toDir,xs[0]),'w').write(etree.tostring(tree))

# saves the info (a list of keys and values: ['key1=val1','key2=val2']
# to the tree. Updates the tags if the already exists, otherwise adds them
def addTag(info,tree):
    info = map(lambda x: x.split('='),info)
    for (tag,val) in info:
        # if it is a year tag, split it into start and begin
        # TODO which encoding? string? int?
        if tag=="year":
           # if the year is not an interval, use same start and end date
           if val.rfind('-')==-1:
              print 'change val'
              val = val+'-'+val
           print val
           interval = val.split('-')
           info += [("begin",interval[0]),("end",interval[1])]
        # else add tag
        else: 
          tit = tree.find(prefix+tag)
          if tit is None:
             tit = etree.SubElement(tree,prefix+tag)
          tit.text = val.decode('utf-8')

filerX = '../filerX/'
prefix = '{http://rtf2xml.sourceforge.net/}'

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
filerna = glob.glob("../filerXNy/*")
def findthem():
    for lst in filerna1:
       for uri in lst:
        print hittaTitel(uri)


