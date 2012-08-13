from django.db import models

class Lemgram(models.Model):
    lemgram  = models.CharField(max_length=100)
    text = models.CharField(max_length=200) 

    def __unicode__(self):
      return self.lemgram

class WrittenForm(models.Model):
    form =  models.CharField(max_length=50)
    lemgrams = models.ManyToManyField(Lemgram)

    def __unicode__(self):
      return self.form


class Word(models.Model):
    word     = models.CharField(max_length=50)
    variants = models.ManyToManyField(WrittenForm)
    #variants = models.ForeignKey(Variant)

    def __unicode__(self):
      return self.word

class Textview(models.Model):
    text  = models.ManyToManyField(Word)
    title = models.CharField(max_length=50)

    def __unicode__(self):
      return self.title


class Variant(models.Model):
    variant  =  models.CharField(max_length=50)
    distance = models.DecimalField
    lemgrams = models.ManyToManyField(Lemgram)

    def __unicode__(self):
      return self.form


