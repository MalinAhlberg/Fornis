from django.db import models

# Create your models here.

class Lemgram(models.Model):
    lemgram  = models.CharField(max_length=100)
    postag   = models.CharField(max_length=20)
    text     = models.CharField(max_length=200)

    def __unicode__(self):
      return self.lemgram

class Word(models.Model):
    word     = models.CharField(max_length=50)
    variants = models.ManyToManyField(Lemgram)

    def __unicode__(self):
      return self.word

class Textview(models.Model):
    text  = models.ManyToManyField(Word)
    title = models.CharField(max_length=50)

    def __unicode__(self):
      return self.title


