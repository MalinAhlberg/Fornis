# -*- coding: utf-8 -*-
import codecs
import re
import os.path

def readtitles(files):
  titledict = {}
  for fil in files:
    with codecs.open(fil,"r",encoding='utf-8') as f:
      for line in f:
        if line.strip():
          xs = line.split('|')
          fil   = os.path.basename(xs[0]).split('.')[0]
          titledict[fil] = {'title':re.search('"(.*)"',xs[1]).group(1)
                           ,'year' :re.search('"(.*)"',xs[2]).group(1)}
  return titledict
      



#filerX/DL.xml |    title="Dalalagen (Äldre Västmannalagen)" | year="1318-1335"
  

