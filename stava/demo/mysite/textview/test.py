from django.http import HttpResponse
from django.template import Context, loader
from textview.models import Lemgram, Textview, Variant, Word
import codecs
from xml.etree import ElementTree as etree
from itertools import chain

textfile = 'SkaL.xml'

def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def start(request):
  return HttpResponse("Now the start test")
  

def viewtextid(request,tid):
  print 'have a id',tid
  return viewtext(request,tid=tid)

def viewtextidvariant(request,tid,variant):
  return viewtext(request,tid=tid,variants=variant)

def viewtext(request,tid=0,variants=''):
    print 'will try to view text',tid
    #txt  = Textview.objects.filter(pk=tid)
    #print 'got',list(''.join(gettext(textfile)).split())[:10]
    wds = ''.join(gettext(textfile)).split()
    #txt  = Textview.objects.filter(pk=tid)
    txt = list(chain(*[Word.objects.filter(word=w) for w in wds]))
    print 'wds',wds[:10]
    print 'did a lookup',txt
    if txt:
      print 'could find it yes'
      #print 'words', txt[0].text.all()
      print 'words', txt[:10]
      t   = loader.get_template('textview/textview.html')
      c = Context({
         'this'      : tid,
         #'text'      : txt,
         'word_list' : txt, #txt[0].text.all(),
      })

      if variants:
        print 'would show a variant view..'
       # html = viewlemgram('',lemgrams) 
        print 'url',variants
        c['varianturl'] = variants
    else:
      print 'cannot find it'
      t = loader.get_template('textview/index.html')
      c = Context({
         'notfound'  : tid,
         'itemtype'  : 'text(er)',
         'itemsort'  : 'textid',
         'index_list': Textview.objects.all(),
      })
    
    return HttpResponse(t.render(c))

def viewvariants(request,wfs):
    print 'in view variants'
    var_dists =  [x.split('_') for x in wfs.split('-')]
    wfs     = [(Variant.objects.get(form=x),d) for x,d in var_dists]
    print wfs
    formlist = [(wf,d, wf.lemgrams.all()) for wf,d in wfs]
    #lemlist = list(chain(*[wf.lemgrams.all() for wf in wfs]))

    print 'will try to view formlist',formlist
    t = loader.get_template('textview/variant.html')
    c = Context({
       'grams' : formlist
    })

    return HttpResponse(t.render(c))


def viewlemgram(request,wfs):
    wfs     = [Variant.objects.filter(form=x) for x in wfs.split('-')]
    lemlist = list(chain(*[wf.lemgrams.all() for wf in list(chain(*wfs))]))

    print 'will try to view lemgram',lemlist
    t = loader.get_template('textview/lemgram.html')
    c = Context({
       'grams' : lemlist
    })

    return HttpResponse(t.render(c))

    #lems = [Lemgram.objects.filter(lemgram=x) for x in wfs.split('-')]

""" reads and collects all text in xml """
def gettext(fil):
    print 'look for file',fil
    xmls = codecs.open('../../../filerX/'+fil,'r').read()
    tree = etree.fromstring(xmls)
    elems  = tree.find('body')
    for e in elems.iter():
#    for e in elems.getiterator():
      if e.tag in ['para','section']:
        old  = e.text or ''
        e.text = ' '+old
    return elems.itertext()


