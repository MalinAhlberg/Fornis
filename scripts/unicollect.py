import glob
import threading
import re
import codecs

# collect unicodes, but script is not yet complete
def normal(c):
  num = ord(c)
  ordok = num in puncts or (num >96 and num<123) or (num>64 and num<91) 
  return c.isdigit() or ordok

def getchars(s,d,uri):
    urid = [] 
    for c in set(s):
      if not normal(c):
        l = d.get(c) or set([])
        l.add(uri)
        d.update({c:l})
        urid.append(c)
    return urid

def doAllNew():
    import os.path
    from xml.etree import ElementTree as etree
    d = {}
    d2 = []
    for uri in glob.glob('../filerX*/*xml'):
    #for uri in ['../filerX/Vidhem.xml']: #glob.glob('../filerX*/*xml'):
      print 'file',uri
      xml  = codecs.open(uri,'r').read()
      tree = etree.fromstring(xml)
      txt  = ''.join(tree.find('body').itertext())
      name = os.path.basename(uri)
      lst  = getchars(txt,d,name)
      lst.sort()
      d2.append(name+'\n'+' '.join(lst)+'\n')

    out = map(lambda x: showpair(x),d.items())
    out.sort()
    d2.sort()
    codecs.open('chars','w',encoding='utf8').write('\n'.join(out))
    codecs.open('charsfile','w',encoding='utf8').write('\n'.join(d2))

def showpair((a,b)):
    files = list(b)
    files.sort()
    return '\t'.join(map(lambda x: unicode(x),[a,ord(a),files]))

puncts = [9,10, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 58
         , 59, 60, 61, 62, 63, 91, 93, 95, 96, 123, 124, 125]
