# -*- coding: utf_8 -*-
import threading
import re       
import glob
import os.path
import xmlparse
import checker
import chunker
import usefuls
from xml.etree import ElementTree as etree
from nltk.tokenize import PunktSentenceTokenizer
import cPickle as pickle

def concatFiles():
    def concater(fil):
      inp = open(uri).read()
      (_,path) = os.path.split(uri)
      out = 'fixedTaggedTest/'+encode(path)
      # concat tags if they are separated by a newpage
      new = xmlparse.use(inp)
      open(out,'w').write(new)
    for uri in usefuls.allFiles:  
        t = threading.Thread(target=concater,args=(uri,))
        t.start()

def pagenumberfixer(uri,segmenter):
    # read file
    inp = open(uri).read()
    (_,path) = os.path.split(uri)
    out = 'fixedTaggedTest/'+encode(path)
    bak = 'sentenceSplit/'+encode(path)
    # concat tags if they are separated by a newpage
    new = xmlparse.use(inp)
    # add here: sentence segmentation
    mode = chunker.findmode(uri)
    chunker.putStops(new,mode,segmenter)
    string = etree.tostring(new,encoding='utf-8')
    open(bak,'w').write(string)
    # fix page numbers
    newer = xmlparse.tagPageN(string)
    # remove bad characters (TODO remove this? might be useful, although dangerous for kark)
    ok1 = re.sub(r'&#x009;','',newer)
    ok  = re.sub(u'¶','',ok1)
    # write file
    print "write file",out
    open(out,'w').write(ok)

def doAll():
    # remove name register
    #for uri in files+filesNy:
    #  fil = open(uri).read()
    #  ok  = re.sub('xmlns="http://rtf2xml.sourceforge.net/"','',fil)  
    #  open(uri,'w').write(ok)

    # add titles etc to xmls
    # titles are not added to NySvenska files
    print "extracting titles"
    newDir = checker.readAndAddInfo(["../titles/titelsExtract.txt","../titles/titelsNyExtract.txt"]) 
     add lables as specified in sections/
    for sec in glob.glob('../sections/*'):
         print "adding label for",sec
         checker.addLabel(sec,newDir)
    # fix the page number issue
    # titles are not added to NySvenska files (newfiles)
    segmenter = getModel()
    for uri in ['../filerX/Apd26SLundversion.xml']: #glob.glob(newDir+'/*') +usefuls.newfiles:  
        t = threading.Thread(target=pagenumberfixer,args=(uri,segmenter))
        t.start()

# fixes weird file paths
def encode(txt):
    dic = {'å':'aa','ä':'ae','ö':'oe',':':'-'}
    for i,j in dic.iteritems():
        txt = txt.replace(i,j)
    return txt

# read model for segmenting
def getModel():
    model = "punkt-nltk-svenska.pickle"
    segmenter = PunktSentenceTokenizer
    with open(model, "rb") as M:
        model = pickle.load(M)
    segmenter_args = (model,)
    segmenter = segmenter(*segmenter_args)
    return segmenter


        
# run this to fix all files
# doAll()

trr = '&#x009;'

def test():
    inp = open("../fixedTagged/Tekla.xml").read()
    tree = etree.fromstring(inp)
    print tree[:10]


