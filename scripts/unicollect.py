import glob
import threading
import re
import codecs

# collect unicodes, but script is not yet complete
def test(s):
    for c in s:
        if ord(c) > 128:
           print "stor"
        else: print "liten"

def test2(s,d):
    r = s
    if s[:2] == '&#':
       t = s 
       x = ''
       while t[:1] != ';':
             x = x+t[:1]
             t = t[1:]
       d[x] = '1'
       r = t
    else: r=s[1:]
    return d,r

def run(s):
    t = s
    d = {}
    while t:
          (d1,r) = test2(t,d)
          d = d1
          t = r
    return d


def collector(uri):
    print "in file",uri
    inp = codecs.open(uri,encoding='utf-8').read()
    xs = tryp(inp)
    inp = codecs.open('hej/'+uri+'unis',encoding='utf-8').write(str(xs))

     
    
files = glob.glob('processed/*')#'scripts/fixed/*')

def collect():
    out = "unis.txt"
    d = {}
    for uri in files:
        print 'working on',uri
        e = collector(uri)
        d.extend(e)
    open('unis','w').write(set(d))

#collect()

def tryp(s):
    l = []
    for c in s:
        #print 'character', c
        try:
          x = ord(c.decode('utf-8'))
          if x> 128:
             l.append(x)
        except UnicodeEncodeError:
             print 'could not decode', c
             l.append(c)
    return l
                
   # r = "&#x*[0-9]*;"
   # return re.findall(r,s)

def collect():
    out = "unis.txt"
    d = {}
    for uri in files:
        print 'working on',uri
        e = collector(uri)
        d.update(e)
    open('unis','w').write(str(d))


def doAll():
    x = []
    for uri in files:
        t = threading.Thread(target=collector,args=(uri,))
        t.start()
 #       x.extend(t.get)

def trans(uri):
    ss = codecs.open(uri,encoding='utf-8').readlines()
    res = map(lambda x: unichr(int(x)),ss)
    for s in res:
        print s, ord(s)
    open('unisar','w').write(str(res))


