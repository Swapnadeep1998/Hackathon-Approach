from django.db import models

# Create your models here.
class Sentiment(models.Model):
    textfield = models.CharField(max_length = 200,null=True)
    
    