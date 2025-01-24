from django.urls import path 
from .controllers import ExempleListCreateView

urlpatterns = [
    path('', PetsList.as_view(), name='pets-list'),
]