from django.conf import settings
from django.db import models

# Create your models here.

class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    # class Meta:
    #     ordering = ('id',)
    #     unique_together = ('list', 'text')
    #
    # def __str__(self):
    #     return self.text