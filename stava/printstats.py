# -*- coding: utf_8 -*-
from extracttxt import shownice
import sys

# (w,[(variant info dist)])

def printstat(wds):
  res = []
  for (i,word) in enumerate(wds):
    j = max(0,i-5)
    context = ' '.join([w[0] for w in wds[j:i+6]])
    res.append((context+'\n'+shownice(word[1],n='\t')+'\t'+word[0]+'\n'))
  return '\n'.join(res)
