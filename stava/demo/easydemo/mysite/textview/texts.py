# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpRequest
from django.template import Context, loader
import generate
from readlex import getthem,readkarklex
from readtitles import readtitles
import glob
import re
import os.path
import urllib
import urlparse

variantdict    = generate.parsemap('../../variantlist')
variantdictman = generate.parsemap('../../smallngb.txt')
variantdictone = generate.parsemap('../../smallngb.txt')
lexframe       = 'lexframe'
titles         = glob.glob('../../../../titles/titels*Extract.txt')

svndict = 'https://svn.spraakdata.gu.se/sb-arkiv/pub/fornsvenska/texter/' 


# Returns page with frames for text and lexical information
def showall(request,fil):
  t = loader.get_template('spelltext/textview.html')
  framename = lexframe 
  c = Context({
      'fil'      : fil,
      'framename': lexframe
   })
  return HttpResponse(t.render(c))

# Returns page with list of all files
def startempty(request):
  titledict = readtitles(titles)
  t     = loader.get_template('spelltext/filelist.html')
  f = urllib.urlopen(svndict)
  s = f.readlines()
  f.close()
  s = getxmlfiles(s)
  files = [getfileinfo(fil,titledict) for fil in s]
  c = Context({
      'files'      : files,
      'svnfiles'   : s})
  return HttpResponse(t.render(c))

# Returns page with all lexicals entries connected to 'words' recieved from karp
def showlexall(request,words):
  t,c = showlexview(request,words,getallentries)
  c['hidecount'] = True
  return HttpResponse(t.render(c))

# Returns page with the lexicals entries from karp identical to 'words'
def showlex(request,words):
  t,c = showlexview(request,words,lexsearch,showrelated=True)
  return HttpResponse(t.render(c))

# Returns page with the lexicals entries for one word 
def onelex(request,word):
  info = lexsearch(word)
  t = loader.get_template('spelltext/lexview.html')
  c = Context({
      'start'      : word,
      'words'      : [word],
      'info'       : info,
      'showrelated': False,
      'hidecount'  : True

   })

  return HttpResponse(t.render(c))

def showlexview(request,words,lookup,showrelated=False):
  wds  = words.split('-')
  info = sum([lookup(w) for w in wds[1:]],[])
  t = loader.get_template('spelltext/lexview.html')
  c = Context({
      'start'      : wds[0],
      'words'      : wds[1:],
      'info'       : info,
      'showrelated': showrelated
   })
  return t,c


# Returns page for a text
def showtextvar(request,var,fil):
  iframe = loader.get_template('spelltext/textview.html')
  c = Context({'framename':lexframe, 'fil':'/text/'+var+'/'+fil})
  return HttpResponse(iframe.render(c))
 
def textvar(request,var,fil):
  if var=='small':
    variant = variantdictman
  elif var=='medium':
    variant = variantdictone
  else:
    variant = variantdict
  path = svndict+fil+'.xml'
  print 'path',path
  body = generate.generatehtml(path,variant,lexframe)
  textframe = loader.get_template('spelltext/textframe.html')
  c = Context({'textpage':body})
  return HttpResponse(textframe.render(c))

# Start view functions
def getfileinfo(fil,fildict):
  filename = os.path.basename(fil).split('.')[0]
  fileinfo = fildict.get(filename,{})
  return filename,fileinfo.get('title',filename),fileinfo.get('year','')

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
        )

def getxmlfiles(html):
  return [x.group(1) for x in (re.search('<a.*>(.*?)\.xml<',line) 
                     for line in html) if x is not None]
  

# Lex view functions
def lexsearch(word):
  return [(word,lexlookup(word).get(word,''))] # TODO should always be in lex..:(

def getallentries(word):
  return lexlookup(word,extralex='fsvm').items() 

def lexlookup(word,extralex=None):
  info = []
  lexs = ['soederwall','schlyter','soederwall-supp']
  if extralex is not None:
    lexs.insert(0,extralex)
  for lex in lexs:
    site = 'http://spraakbanken.gu.se/ws/karp-sok?resurs='+lex+'&wf='+word #+'&format=json'
    site = iriToUri(site)
    f = urllib.urlopen(site)
    info.append((f.read(),lex))
    f.close()
  return readkarklex(info)
# TODO use sw-forms to get only the wanted word probably faster

# not used, could be used if we allow editing of the variants
def remove(word,var):
  worddict = uservar[word]
  del worddict[var]
  generate.printmap(uservar,userfile)
  
  

