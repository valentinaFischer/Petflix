from django.shortcuts import render
from rest_framework import generics
from .models import ExampleModel
from .serializers import ExampleModelSerializer

class PetsList(generics.ListCreateAPIView):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
