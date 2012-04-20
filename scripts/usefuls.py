import re
import glob

# expression for 'utgåvesidonummer':  # 324 
re1 = r'[ >]#\s*[0-9]*'

# expression for 'handskriftssidonummer': [ ‡‡ 31r ] 
# may be surrounded by  '[' ...']' and uses ascii or utf-8 encoding
re2 = re.compile(r"""(\[\s*&\#x2021;&\#x2021;\s*[0-9]*[abrv]*\s*\])|(&\#x2021;&\#x2021;\s*[0-9]*[abrv])|
             (\[\s*&\#8225;&\#8225;\s*[0-9]*[abrv]*\s*\]) |(&\#8225;&\#8225;\s*[0-9]*[abrv])""",re.X)

# old prefix in xml
prefix = '' # "{http://rtf2xml.sourceforge.net/}"

allFiles = glob.glob("../filerX/*xml")+newfiles
newfiles = glob.glob("../filerXNy/*")

filerX = '../filerX/'
