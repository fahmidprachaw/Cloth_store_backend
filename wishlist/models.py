from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    item = models.OneToOneField(Product ,on_delete=models.CASCADE, related_name='wishlist_items')

    def __str__(self) -> str:
        return str(self.item)
