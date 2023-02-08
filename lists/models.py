from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class List(models.Model):
    '''To-Do list identified'''

    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            blank=True,
            null=True,
            on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        '''return absolute url for the object'''
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(item_text, owner=None):
        '''create new list and item'''
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.item_set.first().text

class Item(models.Model):
    '''To-Do list element'''

    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text

