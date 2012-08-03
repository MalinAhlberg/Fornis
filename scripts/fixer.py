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

def pagenumberfixer(uri): #,segmenter):
    # read file
    inp = open(uri).read()
    (_,path) = os.path.split(uri)
    out = 'fixedTaggedTest/'+encode(path)
    bak = 'sentenceSplit/'+encode(path)
    # group paragraphs together if they are separated by a newpage
    new = xmlparse.use(inp,uri)

    # this should be done later, by nice kark-tools
    ## add here: sentence segmentation
    #mode = chunker.findmode(uri)
    #chunker.putStops(new,mode,segmenter)

    string = etree.tostring(new,encoding='utf-8')
    open(bak,'w').write(string)

    # fix page numbers
    newer = xmlparse.tagPageN(string)
    # remove bad characters (TODO remove this? might be useful, although dangerous for kark)
    ok = re.sub(r'&#x009;','',newer)
    #ok  = re.sub(u'¶','',ok1)
    # write file
    print "write file",out
    open(out,'w').write(ok)

def doAll():
    # add titles etc to xmls
    print "extracting titles"
    newDir = checker.readAndAddInfo(["../titles/titelsExtract.txt","../titles/titelsNyExtract.txt"]) 
    #add lables as specified in sections/
    for sec in glob.glob('../sections/*'):
         print "adding label for",sec
         checker.addLabel(sec,newDir)
    for uri in glob.glob(newDir+'/Lydekin*'): # +usefuls.newfiles:  
        t = threading.Thread(target=pagenumberfixer,args=(uri,)) #,segmenter))
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

def removeNameRegister():
    # remove name register
    for uri in files+filesNy:
      fil = open(uri).read()
      ok  = re.sub('xmlns="http://rtf2xml.sourceforge.net/"','',fil)  
      open(uri,'w').write(ok)


        
# run this to fix all files
#doAll()

trr = '&#x009;'

def test():
    import xmlindent
    import codecs
    for fil in glob.glob('../filerX*/*xml'):
      inp = open(fil).read()
      ut  = os.path.join('hej',os.path.basename(fil))
      tree = etree.fromstring(inp)
      xmlindent.indent(tree)
      xml = etree.tostring(tree,encoding='utf8')
      codecs.open(ut,'w').write(xml)
  

