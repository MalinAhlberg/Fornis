import codecs
from extracttxt import shownice

def test():
  xs = open('bigtestallmar','r').readlines()
  ys = open('smalltestallchangesetmar1','r').readlines()
  xs = [prepare(x) for x in xs]
  ys = [prepare(y) for y in ys]
  for (i,x) in enumerate(xs):
    if x and y:# and x!=[''] and y!=['']:
      y = ys[i]
      if y[0]!=x[0]:
        print 'oops, wrong word',i
        break
      else:
        ysbetter = (x[1]=='False' and y[1]=='True') or any([b not in x[2] for b in y[2]])
        if ysbetter:
          codecs.open('analyseres','a',encoding='utf8').write(shownice([[i,x,y]]))
          print i,x,y
          print 'small was better!',i



def prepare(xs):
  if xs and (xs[0]!='*' and xs[0]!='.' and xs.strip('\n \t')!=''):
    if xs[0]=='\t':
      xs = '-'+xs
    ps  = xs.split()
    word = ps[0].strip()
    res = ps[2].strip('() ,')
    lst = [x.strip('()[]') for x in ' '.join(ps[3:]).split('), (')]
    return [word,res,filter(lambda x: x!='None',lst)]
  else:
    return []
