## check which lemgrams and sense-id that are duplicated

from lexiconer import *

def check(fil):
  entries,lexicon = readIt(fil) 
  lex             = lexicon.find('Lexicon')
  lems,senseids = [],[]
  for i,entry in enumerate(entries):
    lemma = entry.find('Lemma')
    lemgram,_ = getAtt(lemma,'lemgram')[0]
    senses  = entry.findall('Sense')
    for sense in senses:
      if sense is not None:
          sid = sense.get('id'):
          if sense.get('id') in senseids:
            print 'sense',sense.get('id')
            sense.set('id',
          else:
            senseids.append(sense.get('id'))
        #[print sid for sid in sense.get('id') if sid in senses]

    if lemgram in lems:
      print 'lemgram',lemgram
    else:
      lems.append(lemgram)

