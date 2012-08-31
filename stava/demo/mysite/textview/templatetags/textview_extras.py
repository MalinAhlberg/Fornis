from django import template

register = template.Library()

@register.filter()
def formatlemgramurl(value):
  path = '/lemgramview/'+value
  return path

@register.filter()
def capitalize(value):
  return value.capitalize()

@register.filter()
def formatformurl(v,text):
  print 'formatformurl!'
  path = '/textid'+text+'/variantview/'
  print path
  link = '-'.join([form.form+'_'+str(d) for (form,d) in getinfo(v) if form is not None])
  print link
  return path+link

def getinfo(v):
  return [(v.variant1,v.distance1),(v.variant2,v.distance2),(v.variant3,v.distance3)]

@register.filter()
def formatvarianturl(value):
  path = '/variants/'+value
  return path


