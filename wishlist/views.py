from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer

# # Create your views here.

# # class WishlistAPIView(generics.RetrieveUpdateAPIView):
# #     serializer_class = WishlistSerializer
# #     permission_classes = [IsAuthenticated]

# #     def get_object(self):
# #         user = self.request.user
# #         queryset = Wishlist.objects.filter(user=user)
# #         if queryset.exists():
# #             return queryset.first()
# #         else:
# #             return Wishlist.objects.create(user=user)
    
# #     def get(self, request, *args, **kwargs):
# #         wishlist = self.get_object()
# #         serializer = self.get_serializer(wishlist)
# #         return Response(serializer.data)

# #     def post(self, request, *args, **kwargs):
# #         product_id = request.data.get('product_id')  # Assuming product_id is sent in the request data
# #         wishlist = self.get_object()
# #         wishlist.products.add(product_id)
# #         return Response({'message': 'Product added to wishlist successfully'})


class WishlistAPIView(viewsets.ViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]


    def get_wishlist(self, user):
        queryset = Wishlist.objects.filter(user=user)
        if queryset.exists():
            return queryset.first()
        else:
            return Wishlist.objects.create(user=user)

    def get(self, request):
        wishlist = self.get_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        wishlist = self.get_wishlist(request.user)
        wishlist.products.add(product_id)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=201)
