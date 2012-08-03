

xml <- readxml
for p in itertext: # ha kvar referens dårå
 for (s,e,varid) in xs: # list of annotations for variation
   divide(p,s,e,varid)

 def divide(p,s,e,varid):
   a,b = p.splitat(s)
   m,r = b.splitat(e)
