from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(primary_key=True)
    pwd = models.CharField(max_length=30)
    rdate = models.DateTimeField()
    udate = models.DateTimeField()

class Documents(models.Model):
    title = models.TextField(max_length=300)
    writer = models.CharField(max_length=200)
    content = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    view_count = models.IntegerField()
    
    
