from django import template

register = template.Library()

@register.filter()
def formatlemgramurl(value,text):
  path = '/textid'+text+'/lemgramview/'
  link = '-'.join([lem.lemgram for lem in value.all()])
  return path+link

@register.filter()
def capitalize(value):
  return value.capitalize()

@register.filter()
def formatformurl(value,text):
  path = '/textid'+text+'/variantview/'
  link = '-'.join([form.form for form in value.all()])
  return path+link


