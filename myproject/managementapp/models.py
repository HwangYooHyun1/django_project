from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(primary_key=True)
    pwd = models.CharField(max_length=30)
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    generation = models.CharField(max_length=100,null=True)

class Documents(models.Model):
    title = models.TextField(max_length=300)
    writer = models.CharField(max_length=200)
    content = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    view_count = models.IntegerField()
    
class Assignments(models.Model):
    title = models.TextField(max_length=300)
    writer = models.CharField(max_length=200)
    content = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    deadline = models.DateTimeField()
    view_count = models.IntegerField()

class Comments(models.Model):
    #assignment가 사라지면 comment도 자동으로 삭제되도록 cascade 지정
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=200)
    content = models.FileField(upload_to='') 
    udate = models.DateTimeField(auto_now_add=True)

class AttendanceNotice(models.Model):
    title = models.TextField(max_length=300)
    writer = models.CharField(max_length=200)
    content = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    view_count = models.IntegerField()

class AttendanceRequest(models.Model):
    title = models.TextField(max_length=300)
    writer = models.CharField(max_length=200)
    request_date = models.DateTimeField()
    request_type = models.CharField(max_length=30)
    content = models.TextField()
    files = models.FileField(upload_to='')
    rdate = models.DateTimeField()
    approval = models.BooleanField(default=False)


