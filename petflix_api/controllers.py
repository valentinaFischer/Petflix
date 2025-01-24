from django.shortcuts import render
from rest_framework import generics, status
from petflix.models import Pet
from .serializers import PetsModelSerializer
from django.contrib.auth.models import User
from .serializers import UserModelSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

# LOGIN
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

# PETS
class PetsListController(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer

class PetsDetailController(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer

class PetsAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=True)
    serializer_class = PetsModelSerializer

# USERS
class UserListController(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            username = user.username
            print(f"Trying to authenticate user: {username}")  # Log de depuração
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                print("Authentication failed")  # Log de depuração
                return Response({'error': 'Wrong credentials'}, status=400)
        except User.DoesNotExist:
            print("User with this email does not exist")  # Log de depuração
            return Response({'error': 'Wrong credentials'}, status=400)

class UserEdit(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print("get_object method called")  # Debugging statement
        # Use the authenticated user from the request
        print(f"Authenticated user: {self.request.user}")
        return self.request.user