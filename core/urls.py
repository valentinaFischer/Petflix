from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('petflix_api.urls')), # Todas as rotas da API começam com /api
]
