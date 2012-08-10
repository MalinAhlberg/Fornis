from django.http import HttpResponse
from django.template import Context, loader
from textview.models import Lemgram, Textview, WrittenForm
from itertools import chain

def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def start(request):
  return HttpResponse("Now the start test")
  

def viewtext(request,tid=0,lemgrams=''):
    print 'will try to view text',tid
    txt  = Textview.objects.filter(pk=tid)
    print 'did a lookup',txt
    if txt:
      print 'could find it yes'
      t   = loader.get_template('textview/textview.html')
      c = Context({
         'this'      : tid,
         'text'      : txt,
         'word_list' : txt[0].text.all(),
      })

      if lemgrams:
        print 'would show a lemgram view..'
        html = viewlemgram('',lemgrams) 
        c['lemgramviews'] = html
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

def viewlemgram(request,wfs):
    wfs     = [WrittenForm.objects.filter(form=x) for x in wfs.split('-')]
    lemlist = list(chain(*[wf.lemgrams.all() for wf in list(chain(*wfs))]))

    print 'will try to view lemgram',lemlist
    t = loader.get_template('textview/lemgram.html')
    c = Context({
       'grams' : lemlist
    })

    return HttpResponse(t.render(c))

    #lems = [Lemgram.objects.filter(lemgram=x) for x in wfs.split('-')]

