from django.shortcuts import render
from rest_framework import generics, status
from petflix.models import Pet
from .serializers import PetsModelSerializer
from django.contrib.auth.models import User
from .serializers import UserModelSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from petflix.models import Pet, AdoptionRequest
from .serializers import RequestSerializer

from .serializers import RequestSerializer

# LOGIN
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

# DELETE
from rest_framework.generics import DestroyAPIView

# PETS
from .serializers import DogSerializer
from .serializers import CatSerializer

class PetsListController(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer

class PetsDetailController(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer

class PetsAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=True)
    serializer_class = PetsModelSerializer

class PetsNotAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=False)
    serializer_class = PetsModelSerializer

class CatsController(generics.ListAPIView):
    queryset = Pet.objects.filter(pet_type="cat")
    serializer_class = PetsModelSerializer

class DogsController(generics.ListAPIView):
    queryset = Pet.objects.filter(pet_type="dog")
    serializer_class = PetsModelSerializer

class CatsNotAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=False, pet_type="cat")
    serializer_class = PetsModelSerializer

class DogsNotAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=False, pet_type="dog")
    serializer_class = PetsModelSerializer

class CatsAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=True, pet_type="cat")
    serializer_class = PetsModelSerializer

class DogsAdoptedController(generics.ListAPIView):
    queryset = Pet.objects.filter(is_adopted=True, pet_type="dog")
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
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)
        
        try:
            user = User.objects.get(username=username)
            print(f"User found: {username}")  # Log de depuração
            
            # Verifique o retorno de authenticate
            user_authenticated = authenticate(username=username, password=password)
            if user_authenticated is not None:
                print(f"Authenticated user: {user_authenticated.username}")  # Log de depuração
                token, created = Token.objects.get_or_create(user=user_authenticated)
                return Response({'token': token.key})
            else:
                print("Authentication failed")  # Log de depuração
                return Response({'error': 'Wrong credentials'}, status=400)
        except User.DoesNotExist:
            print("User with this username does not exist")  # Log de depuração
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
    
class UserDelete(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Aqui, estamos retornando o usuário autenticado para deletá-lo
        return self.request.user

    def perform_destroy(self, instance):
        # Loga a exclusão do usuário
        print(f"User {instance.username} deleted")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        # Sobrescreve o método delete para incluir a resposta personalizada
        self.perform_destroy(self.get_object())
        return Response({"message": "User deleted successfully"}, status=204)
    

# PETS
class PetCreate(APIView):
    def post(self, request, *args, **kwargs):
        pet_type = request.data.get('pet_type')
        if pet_type == 'dog' or pet_type == 'Dog':
            serializer = DogSerializer(data=request.data)
        elif pet_type == 'cat' or pet_type == 'Cat':
            serializer = CatSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid pet type'}, status=400)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class PetDelete(DestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Loga a exclusão do pet
        print(f"Pet {instance.name} deleted")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        # Sobrescreve o método delete para incluir a resposta personalizada
        self.perform_destroy(self.get_object())
        return Response({"message": "Pet deleted successfully"}, status=204)
    
class PetEdit(UpdateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetsModelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        user_id = self.request.user.id
        instance = serializer.save(original_owner=user_id)
        print(f"Pet {instance.name} updated by {self.request.user.username}")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Pet updated successfully"}, status=response.status_code)
    
# REQUESTS

class ReqCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pet_id = request.data.get('pet_id')
        user = self.request.user

        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"error": 'Pet not found'}, status=404)
        
        if pet.original_owner == user:
            return Response({"error": "You are the original owner of this pet."}, status=403)
        
        if pet.is_adopted == True:
            return Response({"error": "You can't adopt an already adopted pet."})
        
        data = request.data.copy()
        data['user_id'] = user.id  # Set the user_id to the authenticated user's ID

        serializer = RequestSerializer(data=data, context={'request': request, 'pet_id': pet_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class MyOwnReqList(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        return AdoptionRequest.objects.filter(user_id=user.id)
    
class MyPetsReqList(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  
        pets_owned_by_user = Pet.objects.filter(original_owner=user)
        pet_ids = pets_owned_by_user.values_list('id', flat=True)
        return AdoptionRequest.objects.filter(pet_id__in=pet_ids)
    
class TreatReq(generics.UpdateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user  
        pets_owned_by_user = Pet.objects.filter(original_owner=user)
        pet_ids = pets_owned_by_user.values_list('id', flat=True)
        # Filter the AdoptionRequest objects based on the pet IDs
        return AdoptionRequest.objects.filter(pet_id__in=pet_ids)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'approved':
            pet = instance.pet
            pet.is_adopted = True
            pet.save()

class ReqDelete(generics.DestroyAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Loga a exclusão do pet
        print(f"Request {instance.id} deleted")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        # Sobrescreve o método delete para incluir a resposta personalizada
        self.perform_destroy(self.get_object())
        return Response({"message": "Request deleted successfully"}, status=204)