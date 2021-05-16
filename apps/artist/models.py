from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='artist', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_balance(self):
        items = self.items.filter(artist_paid=False, order__artists__in=[self.id])
        return sum((item.artwork.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(artist_paid=True, order__artists__in=[self.id])
        return sum((item.artist.price * item.quantity) for item in items)