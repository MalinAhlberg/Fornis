# -*- coding: utf_8 -*-
from extracttxt import shownice

# [(word, (numbers,(directly,vars)))] -> ok: [wds]{10} \n lemgram, dist
# som	(253, (False, (u'som', 'som..e.1')))
# oppenbarilse	(4, (True, [(u'oppenbarilse', 'opinbarilse', 1.5, 'opinbarilse..nn.1')]))
# joannis	(5, (False, None))
def printstat(xs):
  def output(i,x):
     w,(n,(b,lst)) = x
     if b==False and lst==None:
       return ''
     else:
       j = max(0,i-5)
       wds = ' '.join(map(lambda (w,z): w,xs)[j:i+6])
       res = shownice(format(b,lst),t='  ',n='\t')
       return wds+'\n'+res+' ('+w+')'+'\n'
  return '\n'.join([output(i,x) for (i,x) in enumerate(xs)])

# bool,xs -> [(lemgram,distance)] (3 st)
def format(b,lst):
  if not b: 
    return map(lambda (w,lemgram): (lemgram,0),[lst])
  else:
    return map(lambda (w,var,d,lemgram): (lemgram,d),lst[:3])

    
