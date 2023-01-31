from django.db import models
from django.urls import reverse

# Create your models here.
class List(models.Model):
    '''To-Do list identified'''

    def get_absolute_url(self):
        '''return absolute url for the object'''
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    '''To-Do list element'''

    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text

