from django.http import HttpResponse
from django.template import Context, loader
from textview.models import Lemgram, Textview

def index(request):
    return HttpResponse("Hello, world. You're at the test index.")

def start(request):
  return HttpResponse("Now the start test")
  

def viewtext(request,tid):
    print 'will try to view text',tid
    txt  = Textview.objects.filter(pk=tid)
    print 'did a lookup',txt
    if txt:
      print 'could find it'
      t   = loader.get_template('textview/textview.html')
      wds = t.text_set.all()
      c = Context({
         'text'      : txt,
         'word_list' : wds,
      })

    else:
      print 'cannot find it'
      t = loader.get_template('textview/index.html')
      txtlist  = Textview.objects.all()
      c = Context({
         'notfound' : tid,
         'index'    : txtlist,
      })

    return HttpResponse(t.render(c))

