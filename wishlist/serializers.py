from rest_framework import serializers
from . import models


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = '__all__'