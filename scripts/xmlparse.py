# -*- coding: utf_8 -*-

import re
import os.path
from xml.etree import ElementTree as etree
from usefuls import *

fil  =  "../filerX/Alexius.xml"

testxml = '''
          <doc>
          <body>
          <para><inline1 font-size="12.00"
          font-style="Times"># 219 jak h&#xF6;rde aaf tinom wisdom och deylighet sakth,
          </inline1></para>
          <para><inline2 font-size="12.00"
          font-style="Times"># 220 
          </inline2></para>
          <para><inline3 font-size="12.00"
          font-style="Times"># 221 tre
          </inline3></para>
          <para><inline3 font-size="12.00"
          font-style="Times">221 tre
          </inline3></para>
          <para><inline3 font-size="12.00"
          font-style="Times">hej hu
          </inline3></para>
          </body>
          </doc>
            '''

# makes sure that a paraghraph is not interrupted by a pagebreak
def use(xmls,fil):
    etree.register_namespace('',prefix)
    tree = etree.fromstring(xmls)
    makeParagraphs(tree.find(prefix+'body'),fil)
    return tree
    #return etree.tostring(tree)

###############################################################################
# Groups 'para's into 'paragraphs', where paras split by pagebreaks
# are put into the same paragraph
###############################################################################

def makeParagraphs(body,fil):
    # find all paras
    paras = body.findall('section/paragraph-definition/para')
    appendNext = False
    paralist = []
    thispara = []
    for para in paras:
        #print 'paragraph',list(para.itertext())
        if len(list(para.itertext()))!=0:
            if ispagebreak(para) or appendNext:
                # append this element to last list
                thispara.append(para)
                # if this element is only a pagebreak, continue with next element
                if isonlypagebreak(para):
                    appendNext = True
                else:
                    # otherwise, we don't need to append
                    appendNext = False
            # only for Lydekin, which has special paragraphs
            elif lydekinpagebreak(para,fil): 
                    thispara.append(para)
                    appendNext = True
            else:
                # end last paragraph, and start a new containing this element
                paralist.append(thispara)
                thispara = [para]


    # add the last paragraph to the list
    paralist.append(thispara)

    # remove all old paragraphs from the body
    paras = body.findall('section')
    for para in paras:
        body.remove(para)

    # now add all paragraphs enclosed in 'paragraph' elements
    for para in paralist:
        elem = etree.SubElement(body,'paragraph')
        map(lambda p: elem.append(p), para)

###############################################################################
# Creates pagenumber tags
###############################################################################

# TODO nicer pagenumbering! not be nested with para-tag (end before and add
# one if necessary. or can we just add simple nodes and let karkish deal with
# it?
#def addPageNum(tree):
#    tagPageNum(tree.find(prefix+'body'))
#    paras = body.findall('section/paragraph-definition/para')
#    pnum = None
#    hnum = None
#    for para in paras:
#        # move all in para to a num (pnum, hnum tag)
#        # put this in para




# creates tags for pagenumbering in body
# maunal subsitution in xml. not safe, produces nested tags which are
# not accepted in standard xml
def tagPageN(tree):
    # we only want to change the body
    parts = re.split('<body>',tree,2)
    # and we want to close all page numbering-tags befor the body ends
    body = re.split('</body>',parts[1])
    # tag creation
    xml = tagPageNo(body[0])
    return parts[0]+'<body>'+xml+'</body>'+body[1]

# creates tags for pagenumbering
# maunal subsitution in xml. not safe, produces nested tags which are
# not accepted in standard xml
def tagPageNo(tree):
         i = 0 # position in string
         # inserts an element surrounded by text
         def insert(txt,pos,pos2,elem):
             return txt[:pos]+elem+txt[pos2:]

         # finds 'reg' in 'tree' (after position 'i') and inserts a tag 
         # of type 'typ' at the position of 'reg'
         def inserts(tree,typ,reg,i,close):
               newtree = tree
               while True:
                 m = re.search(reg,newtree[i:])
                 if m:
                    (st,end) = m.span()
                    num      = extractNo(m.group())
                    newelem = makeelem(typ,num,m.group()[:1],close)
                    newtree = insert(newtree,st+i,end+i,newelem)
                    close = True
                    i = i+end+len(newelem)
                 else: break
               return (newtree,close)

        # produces end tags if necessary
         def closeTag(tag,s,close):
             if close:
                return s+'</'+tag+'>'
             else: return s

         # insert tags for 'utgåvesidonummer'
         (t1,c)  = inserts(tree,"pagenum",re1,0,False)
         # end open tags
         t2      = closeTag("pagenum",t1,c)

         # insert tags for 'handskriftsidonummer'
         (t3,c1) = inserts(t2,"hskr",re2,0,False)
         # end open tags
         t4      = closeTag("hskr",t3,c1)
         return t4


##############################################################################
# Help functions
##############################################################################


# decides whether an element consists of more than just a pagebreak-symbol
def isonlypagebreak(elem):
    s = extractText(elem).strip()
    pagnumbers = '(\s*'+p1+'\s*$)|'+'(\s*'+p2+'\s*$)|'+'(\s*'+p3+'\s*$)'
    pbreak = re.search('\s*'+pagenumbers+'\s*$',' '+s,re.U)
    return pbreak is not None

def lydekinpagebreak(elem,fil):
    if os.path.basename(fil)=='Lydekin.xml':
      print 'Lydekin yes'
      s = extractText(elem).strip()
      lydekin = '\[*?\]$'
      pbreak = re.search(lydekin,s,re.U)
      if pbreak is not None: print 'found a false pb'
      return pbreak is not None
    return False

def ispagebreak(elem):
    text = extractText(elem)
    stripped = text.strip()
    p1 = stripped[0:1]=='#'
    p2 = re.match(u'\[*\s*‡',stripped,re.U)
    return p1 or p2

# extracts all texts from an element
def extractText(elem):    
    return ''.join(list(elem.itertext()))

# creates a tag, possibly after having closed earlier tag
# and reinserting end-brackets ('>')
def makeelem(tag,att,opt,close):
    x = closer = ''
    if opt=='>':
       x = '>'
    if close:
       closer = '</'+tag+'>'
    return x+closer+'<'+tag+' num=\"'+att+'\" >'

# extracts the pagenumber from a handskriftssidonummer and pagenumber
def extractNo(s):
    ok  = re.sub(hskTag,'',s)  
    return ''.join(filter(lambda x: x.isdigit() or x.isalpha(),ok))
    

             
hskTag = r'(&#x2021;&#x2021;)|(&#8225;&#8225;)' 
utfilen = "kalas.xml"
#open(utfilen,'w').write(use(open(fil).read()))


##############################################################################
# Tests
##############################################################################

def test():
    tree = etree.fromstring(testxml)
    _ = concatTags(tree.find('body'))
    print etree.tostring(tree)

def test2():
    tree = etree.fromstring(testxml)
    para = tree.find('body').find('para1').find('inline1')
    para.insert(1,tree.makeelement('num',{'p':'1'}))
    return etree.tostring(tree)
    #print etree.tostring(tree)

def test3(uri):
    fil = open(uri,'r').read()
    tree = etree.fromstring(fil)
    makeParagraphs(tree.find('body'))
    open('kast.xml','w').write(etree.tostring(tree))


def makeelemm(tag,att,val):
    return '<'+tag+att+'='+val+'>'


##############################################################################
# Not used
##############################################################################

# concatenates text in tags if they are interrupted by pagebreak
# not used atm
def concatTags(tree,p = None):
# TODO do this on paras only
    pOld = p
    for elem in tree:
      # if the last element is appendable and if this one start with # ...
      if p!=None and elem.text and ispagebreak(elem.text):
         # then move text to last element and empty this
         p.text = p.text +' '+ elem.text 
         elem.text = ""
      # else, check whether this element is appendable
      elif elem.text and elem.text.strip():
         p = elem
      # then go through inner trees
      p1 = concatTags(elem,p)
      p = p1
    return p


