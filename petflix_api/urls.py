from django.urls import path 
from .controllers import PetsListController, UserEdit
from .controllers import PetsDetailController
from .controllers import PetsAdoptedController
from .controllers import UserListController
from .controllers import UserCreate
from .controllers import UserLogin

urlpatterns = [
    path('', PetsListController.as_view(), name='pets-list'),
    path('<int:pk>/', PetsDetailController.as_view(), name='pets-detail'),
    path('adopted/', PetsAdoptedController.as_view(), name='pets-adopted'),

    path('users/', UserListController.as_view(), name='users-list'),
    path('create-user/', UserCreate.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('users/edit/', UserEdit.as_view(), name='user-edit'),
]