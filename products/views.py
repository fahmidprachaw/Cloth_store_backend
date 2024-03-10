from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User
from django_filters import filters
from . import models
from . serializers import ProductSerializer, ReviewSerializer, RegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.


# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = models.Product.objects.all()
#     serializer_class = ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'popularity']
    filterset_fields = ['size', 'color']


# generics.CreateAPIView
class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = models.Product.objects.all()
#     serializer_class = ProductSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         reviews = Review.objects.filter(product=instance)
#         avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
#         product_data = self.get_serializer(instance).data
#         product_data['avg_rating'] = avg_rating
#         product_data['reviews'] = ReviewSerializer(reviews, many=True).data
#         return Response(product_data)
        

# class UserRegistrationApiView(APIView):
#     serializer_class = RegistrationSerializer
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
        
#         if serializer.is_valid():
#             user = serializer.save()
#             print(user)
#             token = default_token_generator.make_token(user)
#             print("token ", token)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             print("uid ", uid)
#             return Response("Check your mail for confirmation")
#         return Response(serializer.errors)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data) # form er moto kore 
    #     #serializer er user er request kora data gula capture korlam
        
    #     if serializer.is_valid(): # json data valid hoile er condition e jabe
    #         user = serializer.save()
    #         return Response("Form Submission Done")
    #     return Response(serializer.errors)
        
class UserRegistrationViewSet(viewsets.ViewSet):
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"https://cloth-store-backend.onrender.com/products/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# def activate(request, uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode()
#         user = User._default_manager.get(pk=uid)
#     except(User.DoesNotExist):
#         user = None 
    
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('login')
#     else:
#         return redirect('register')
    
from django.http import HttpResponseNotFound

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  # Assuming 'login' is the name of your login URL
    else:
        return HttpResponseNotFound("Activation link is invalid or expired.")

    
# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data = self.request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             user = authenticate(username= username, password=password)
            
#             if user:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 print(token)
#                 print(_)
#                 login(request, user)
#                 return Response({'token' : token.key, 'user_id' : user.id})
#             else:
#                 return Response({'error' : "Invalid Credential"})
#         return Response(serializer.errors)
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                # User is authenticated, generate token
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                # Authentication failed, return error message
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Serializer validation failed, return error details
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
         # return redirect('login')
        return Response({'success' : "logout successful"})