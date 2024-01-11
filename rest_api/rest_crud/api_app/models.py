from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=150)
    photo = models.FileField()
    status = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
