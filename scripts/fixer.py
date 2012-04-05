# -*- coding: utf_8 -*-
import threading
import re       
import glob
import os.path
import xmlparse

txt = ''' super
          sträng (bra för lines)'''


def opener(uri):
    # read file
    inp = open(uri).read()
    (_,path) = os.path.split(uri)
    out = 'fixed/'+encode(path)
    # fix page numbers
    new = xmlparse.use(inp)
    # remove ugly tags
    ok1 = re.sub('ns0:','',new)  
    ok  = re.sub(r'&#x009;','',ok1)  
    # write file
    print 'writing to', out
    open(out,'w').write(ok)

files = glob.glob('../filerX/*.xml')
# ['../filerX/Troja.xml'] # 

def doAll():
    for uri in files:
        t = threading.Thread(target=opener,args=(uri,))
        t.start()

def trim():
    for uri in files:
        t = threading.Thread(target=trimmer,args=(uri,))
        t.start()

def trimmer(uri):
    # read file
    inp = open(uri).read()
    (_,path) = os.path.split(uri)
    out = 'trimmed/'+ encode(path)
    # remove characthers
    ok  = re.sub(r'&#x009;','',inp)  
    # write file
    print 'writing to', out
    print ok
    open(out,'w').write(ok)

def encode(txt):
    for i,j in dic.iteritems():
        txt = txt.replace(i,j)
    return txt

dic = {'å':'aa','ä':'ae','ö':'oe'}
        
#trim()
doAll()

trr = '&#x009;'
