from django.db import models

class Style(models.Model):
    subject = models.CharField(max_length=64)
    date = models.DateField() # datetime->date 
    category = models.CharField(max_length=16)
    views = models.IntegerField(default=0)
    URL = models.TextField(null=True)
    tag = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
