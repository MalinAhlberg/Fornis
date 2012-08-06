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
#      Formrepresentation 
#           partOfSpeech = "nn"           bara en viss uppsätting av taggar får vara här
#                                         resten får vara i information
#           lemgram      = "katt..nn.1"   inga 'e'n, om det finns '*' eller '?' tas de bort och indexet uppdateras
#           gram         = "m."           här kan annan grammatisk information finnas
#                                         typ 'm.' (och 'med dat.'?)
#           information  =                här får annat bös vara
#           writtenForm =                 en eller två (fler?) ord, inga paranteser 
#                                         eller andra tecken, siffror...
#                                         ta bort överblivna kommatecken, punkter och mellanslag
#                                         (söderwall)
#           information =                 annan text som inte ska vara i writtenForm (söderwall)
#                                         ev flytta hit efter förfrågan
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
#                                    borde städas, och eventuellt flyttas.
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
#      id                            inga '*' eller '?', tas bort om de finns och indexet uppdateras
#      Definition                    lite vad som helst
#      \Definition
#   \Sense
#   Sense
#      Definition
#      \Definition
#   \Sense
#


######### STEP 2

# få ut varianter från wordform.
# De ligger i LexicalEntry - WordForm - writtenForm
# måste städas (ta bort kolon, paranteser mm, och också luras på så att man inte får med efterföljande ord
# sedan borde de kopieras till LexicalEntry - WordForm - variation. bara det bra, det dåliga kan få ligga kvar.
# men hur vem man om det är bra?
