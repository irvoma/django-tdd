from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['text', 'list'], name='unique_item_in_list'),
        ]

    def __str__(self):
        return self.text
