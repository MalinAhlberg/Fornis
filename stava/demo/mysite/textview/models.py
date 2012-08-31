from django.db import models

class Lemgram(models.Model):
    lemgram    = models.CharField(max_length=100)
    #dictionary = models.CharField(max_length=50)
#    text     = models.CharField(max_length=200) 

    def __unicode__(self):
      return self.lemgram


class Variant(models.Model):
    form     = models.CharField(max_length=50)
    lemgrams = models.ManyToManyField(Lemgram)

    def __unicode__(self):
      return self.form


class Word(models.Model):
    word     = models.CharField(max_length=50)
    variant1 = models.ForeignKey(Variant,related_name='1',null=True)
    variant2 = models.ForeignKey(Variant,related_name='2',null=True)
    variant3 = models.ForeignKey(Variant,related_name='3',null=True)
    distance1 = models.IntegerField() 
    distance2 = models.IntegerField() 
    distance3 = models.IntegerField() 

    def __unicode__(self):
      return self.word


#
#class Textview(models.Model):
#    text  = models.ManyToManyField(Word)
#    title = models.CharField(max_length=50)
#
#    def __unicode__(self):
#      return self.title
#

# TODO start using this instead of WrittenForm
# or have WF in between..? Adapt db and views to use this!

#class WrittenForm(models.Model):
#    form =  models.CharField(max_length=50)
#    lemgrams = models.ManyToManyField(Lemgram)
#
#    def __unicode__(self):
#      return self.form


#class Word(models.Model):
#    word     = models.CharField(max_length=50)
#    variants = models.ManyToManyField(WrittenForm)
#    #variants = models.ForeignKey(Variant)
#
#    def __unicode__(self):
#      return self.word


