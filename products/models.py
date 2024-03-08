from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

SIZE_SELECT = [
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL')
]

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/media/')
    size = models.CharField(choices = SIZE_SELECT ,max_length=20)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class Review(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    rating = models.CharField(choices = STAR_CHOICES, max_length=20)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.user.first_name}'
    