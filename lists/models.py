from django.db import models

# Create your models here.
class Item(models.Model):
    '''To-Do list element'''

    text = models.TextField(default='')
