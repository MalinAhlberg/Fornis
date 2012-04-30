# -*- coding: utf_8 -*-
import re
import glob

# expression for 'utgåvesidonummer':  # 324 
re1 = r'[\s>]#\s*[0-9]+'

# expression for 'handskriftssidonummer': [ ‡‡ 31r ] 
# may be surrounded by  '[' ...']' and uses ascii or utf-8 encoding
re2 = re.compile(r"""(\[\s*&\#x2021;&\#x2021;\s*[0-9]+[abrv]*\s*\])|(&\#x2021;&\#x2021;\s*[0-9]+[abrv])|
             (\[\s*&\#8225;&\#8225;\s*[0-9]+[abrv]*\s*\]) |(&\#8225;&\#8225;\s*[0-9]+[abrv])""",re.X)

# old prefix in xml
prefix = '' # "{http://rtf2xml.sourceforge.net/}"

newfiles = glob.glob("../filerXNy/*")
allFiles = glob.glob("../filerX/*xml")+newfiles

concatFiles = glob.glob("concattedParas/*xml")

filerX = '../filerX/'

p1  = u'\[[\s>]#\s*[0-9]+\]'
p1a =   u'[\s>]#\s*[0-9]+'
p2  = u'\[\s*‡‡\s*[0-9]+\s*[abrv]*\s*\]'
p3  =      u'‡‡\s*[0-9]+[abrv]*'
pagenumbers = '('+p1+')|('+p2+')|('+p3+')'
