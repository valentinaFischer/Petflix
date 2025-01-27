from django.urls import path 
from .controllers import PetsListController, UserEdit
from .controllers import PetsDetailController
from .controllers import PetsAdoptedController
from .controllers import UserListController
from .controllers import UserCreate
from .controllers import UserLogin
from .controllers import UserDelete
from .controllers import PetCreate
from .controllers import PetDelete
from .controllers import PetEdit
from .controllers import PetsNotAdoptedController
from .controllers import CatsController
from .controllers import DogsController
from .controllers import CatsNotAdoptedController
from .controllers import DogsNotAdoptedController
from .controllers import CatsAdoptedController
from .controllers import DogsAdoptedController
from .controllers import ReqCreate
from .controllers import MyOwnReqList
from .controllers import MyPetsReqList
from .controllers import TreatReq
from .controllers import ReqDelete

urlpatterns = [
    path('', PetsListController.as_view(), name='pets-list'),
    path('<int:pk>/', PetsDetailController.as_view(), name='pets-detail'),
    path('adopted/', PetsAdoptedController.as_view(), name='pets-adopted'),
    path('available/', PetsNotAdoptedController.as_view(), name='available'),
    path('dogs/', DogsController.as_view(), name='dogs'),
    path('cats/', CatsController.as_view(), name='cats'),
    path('available/cats/', CatsNotAdoptedController.as_view(), name='available-cats'),
    path('available/dogs/', DogsNotAdoptedController.as_view(), name='available-dogs'),
    path('adopted/dogs/', DogsAdoptedController.as_view(), name='adopted-dogs'),
    path('adopted/cats/', CatsAdoptedController.as_view(), name='adopted-cats'),

    path('users/', UserListController.as_view(), name='users-list'),
    path('create-user/', UserCreate.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('users/edit/', UserEdit.as_view(), name='user-edit'),
    path('users/delete/', UserDelete.as_view(), name='user-delete'),

    path('pet/create/', PetCreate.as_view(), name='pet-create'),
    path('pet/delete/<int:id>/', PetDelete.as_view(), name='pet-delete'),
    path('pet/edit/<int:id>/', PetEdit.as_view(), name='pet-edit'),

    path('request/create/', ReqCreate.as_view(), name="request-create"),
    path('requests/', MyOwnReqList.as_view(), name='my-requests'),
    path('requests-for-my-pets/', MyPetsReqList.as_view(), name='MyPetsReqList'),
    path('requests/<int:id>/treat/', TreatReq.as_view(), name='treat-request'),
    path('request/delete/<int:id>/', ReqDelete.as_view(), name='req-delete')
]