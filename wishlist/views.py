from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer


# # Create your views here.



class WishlistViewSet(viewsets.ViewSet):
    serializer_class = WishlistSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        if 'product_id' not in request.data:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data['product.id']

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Invalid product_id'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        wishlist.item_id = product_id
        wishlist.save()

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class WishlistItemsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            wishlist = Wishlist.objects.filter(user=user).first()
            return [wishlist.item]
        except Wishlist.DoesNotExist:
            return []
        

class AddToWishlistAPIView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        wishlist, created = Wishlist.objects.get_or_create(user=user)
        wishlist.products.add(product)

        return Response({'success': 'Product added to wishlist'}, status=status.HTTP_201_CREATED)


