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
def formatformurl(value,text):
  path = '/textid'+text+'/variantview/'
  link = '-'.join([form.form for form in value.all()])
  return path+link


