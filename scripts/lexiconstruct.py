# * ?   vad betyda, ta bort eller byt, fixa
# namnbyten:
# lem -> lemgram (done! by jonatan)
# gram -> partOfSpeech
# pos-taggar borde döpas om

# flytta ut pos och lemgram från Formrep
# hitta 'e':n med de två sätten
# peka ut vad som avviker från detta:

# LexicalEntry
#   Lemma
#      partOfSpeech = "nn"           bara en viss uppsätting av taggar får vara här
#                                    resten får vara i information
#      lemgram      = "katt..nn.1"   inga 'e'n
#      gram         = "m."           här kan annan grammatisk information finnas
#                                    typ 'm.' (och 'med dat.'?)
#      information  =                här får annat bös vara
#      Formrepresentation 
#           writtenForm =            en eller två (fler?) ord, inga paranteser 
#                                    eller andra tecken, siffror...
#                                    ta bort överblivna kommatecken, punkter och mellanslag
#                                    (söderwall)
#           information =            annan text som inte ska vara i writtenForm (söderwall)
#                                    ev flytta hit efter förfrågan
#      \Formrepresentation 
#      Formrepresentation 
#           writtenForm = 
#      \Formrepresentation 
#   \Lemma
#   WordForm
#      gram = "pl"                   ska den heta gram? bara vissa taggar ok
#                                    skulle också kunna ta ut info: (klurigt pga oording!)
#                                      gram : '2 pers' => person = '2'
#                                    anta att det alltid först kommer gram och sen dess former?
#                                    svårt med förled etc. får nog vara information om det inte passar
#      Formrepresentation 
#           writtenForm =            en eller två (fler?) ord, inga paranteser osv, städa!
#           information =            annan text som inte ska vara i writtenForm
#                                    ev flytta hit efter förfrågan
#      \Formrepresentation 
#      Formrepresentation 
#           writtenForm = 
#      \Formrepresentation 
#   \WordForm
#   WordForm
#      gram = "sg"
#      Formrepresentation 
#           writtenForm = 
#      \Formrepresentation 
#      Formrepresentation 
#           writtenForm = 
#      \Formrepresentation 
#   \WordForm
#   Sense                       
#      Definition                    lite vad som helst
#      \Definition
#   \Sense
#   Sense
#      Definition
#      \Definition
#   \Sense
#

# Alla borde ha åtminstone ok Lemma, pos, lemgram, WrittenForm
# varianter kan flyttas automatiskt (schlyter)
# flytta annat bös till subnod?  
# (obs, saldo har annan ording, pos och lemgram ligger i formrepr.)
