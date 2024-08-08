from django.db import models

# Create your models here.
#
class Sentiment(models.Model):

    given_text = models.TextField()
    sentiment_score = models.FloatField()
    sentiment = models.CharField(max_length=50)

    def __str__(self):
        return self.sentiment

class logindatabase(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
