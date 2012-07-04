import cc

def spellcheck(w,lex,alpha,edit,distance,number):
  res = []

  for cc in getchanges(w,d,alpha):
    for (c,lem) in dict(cc).items():
      dist = edit_dist(w,c,rules=edit[0],n=edit[1]) if edit else edit_dist(w,c) 
      if dist<distance:
        var.append((w,c,dist,lem))
  res.sort(key=lambda (w,c,dist,lem): dist)

  return res[:number]


