from django.db import models

# Create your models here.
class List(models.Model):
    '''To-Do list identified'''

    pass

class Item(models.Model):
    '''To-Do list element'''

    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

