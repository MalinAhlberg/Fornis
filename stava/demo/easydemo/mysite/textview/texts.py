from django.http import HttpResponse
from django.template import Context, loader
import generate
from readlex import getthem
import glob
import os.path


variantdict = generate.parsemap('../../../variantlist')
variantdictman = generate.parsemap('../../../smallngb.txt')
variantdictone = generate.parsemap('../../../smallngb.txt')
lexframe       = 'lexframe'
lexicon = getthem()


def showall(request,fil):
  t = loader.get_template('spelltext/textview.html')
  framename = lexframe 
  c = Context({
      'fil'      : fil,
      'framename': lexframe
   })
  return HttpResponse(t.render(c))
 

def startempty(request):
  t     = loader.get_template('spelltext/filelist.html')
  files = [os.path.basename(fil).split('.')[0] for fil in glob.glob('../../../../filerX/'+'*xml')]
  c = Context({
      'files'      : files})
  return HttpResponse(t.render(c))

def showlex(request,words):
  wds  = words.split('-')
  info = [(w,lexicon.get(w,[])) for w in wds[1:]]
  t = loader.get_template('spelltext/lexview.html')
  c = Context({
      'start'      : wds[0],
      'words'      : wds[1:],
      'info'       : info
   })
  return HttpResponse(t.render(c))

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
  iframe = loader.get_template('spelltext/textview.html')
  path = '../../../../filerX/'+fil+'.xml'
  body = generate.generatehtml(path,variant,lexframe)
  return HttpResponse(header+body)

  
  
header = """
<style>
  body { color : grey; }
  a { color : black; text-decoration:none; }
  a:hover { color : blue; }
</style>"""


# Dead code
#
#def viewtextid(request,tid):
#  print 'have a id',tid
#  return viewtext(request,tid=tid)
#
#def viewtextidvariant(request,tid,variant):
#  return viewtext(request,tid=tid,variants=variant)
#
#def viewtext(request,tid=0,variants=''):
#    print 'will try to view text',tid
#    #txt  = Textview.objects.filter(pk=tid)
#    #print 'got',list(''.join(gettext(textfile)).split())[:10]
#    wds = ''.join(gettext(textfile)).split()
#    #txt  = Textview.objects.filter(pk=tid)
#    txt = list(chain(*[Word.objects.filter(word=w) for w in wds]))
#    print 'wds',wds[:10]
#    print 'did a lookup',txt
#    if txt:
#      print 'could find it yes'
#      #print 'words', txt[0].text.all()
#      print 'words', txt[:10]
#      t   = loader.get_template('textview/textview.html')
#      c = Context({
#         'this'      : tid,
#         #'text'      : txt,
#         'word_list' : txt, #txt[0].text.all(),
#      })
#
#      if variants:
#        print 'would show a variant view..'
#       # html = viewlemgram('',lemgrams) 
#        print 'url',variants
#        c['varianturl'] = variants
#    else:
#      print 'cannot find it'
#      t = loader.get_template('textview/index.html')
#      c = Context({
#         'notfound'  : tid,
#         'itemtype'  : 'text(er)',
#         'itemsort'  : 'textid',
#         'index_list': Textview.objects.all(),
#      })
#    
#    return HttpResponse(t.render(c))
#
#def viewvariants(request,wfs):
#    print 'in view variants'
#    var_dists =  [x.split('_') for x in wfs.split('-')]
#    wfs     = [(Variant.objects.get(form=x),d) for x,d in var_dists]
#    print wfs
#    formlist = [(wf,d, wf.lemgrams.all()) for wf,d in wfs]
#    #lemlist = list(chain(*[wf.lemgrams.all() for wf in wfs]))
#
#    print 'will try to view formlist',formlist
#    t = loader.get_template('textview/variant.html')
#    c = Context({
#       'grams' : formlist
#    })
#
#    return HttpResponse(t.render(c))
#
#
#def viewlemgram(request,wfs):
#    wfs     = [Variant.objects.filter(form=x) for x in wfs.split('-')]
#    lemlist = list(chain(*[wf.lemgrams.all() for wf in list(chain(*wfs))]))
#
#    print 'will try to view lemgram',lemlist
#    t = loader.get_template('textview/lemgram.html')
#    c = Context({
#       'grams' : lemlist
#    })
#
#    return HttpResponse(t.render(c))
#
#    #lems = [Lemgram.objects.filter(lemgram=x) for x in wfs.split('-')]
#
#""" reads and collects all text in xml """
#def gettext(fil):
#    print 'look for file',fil
#    xmls = codecs.open('../../../filerX/'+fil,'r').read()
#    tree = etree.fromstring(xmls)
#    elems  = tree.find('body')
#    for e in elems.iter():
##    for e in elems.getiterator():
#      if e.tag in ['para','section']:
#        old  = e.text or ''
#        e.text = ' '+old
#    return elems.itertext()
#
##  
#def start(request,fil):
#  print 'start'
#  t = loader.get_template('spelltext/textview.html')
#  c = Context({
#      'fil'      : 'text/'+fil,
#   })
#  return HttpResponse(t.render(c))
 
#                              ,'/home/malin/Spraak/Lexicon/good/lmf/soederwall/soederwall.xml'
#                              ,'/home/malin/Spraak/Lexicon/good/lmf/soederwall_supp/soederwall_supp.xml'])
#def showtext(request,fil):
#  #path = '../../../../filerX/'+fil+'.xml'
#  #html   = generate.generatehtml(path,variantdict,'lexframe')
#  iframe = loader.get_template('spelltext/textview.html')
#  c = Context({'framename':'lexframe', 'fil':'/text/'+fil})
#  return HttpResponse(iframe.render(c))
 
#def text(request,fil):
#  path = '../../../../filerX/'+fil+'.xml'
#  body = generate.generatehtml(path,variantdict,'lexframe')
#  return HttpResponse(header+body)
#  
#def textsmall(request,fil):
#  path = '../../../../filerX/'+fil+'.xml'
#  body = generate.generatehtml(path,variantdictman,'lexframe2')
#  return HttpResponse(header+body)
   
