from django.contrib import admin

# Register your models here.
from petflix.models import Pet, Dog, Cat  

admin.site.register(Pet)
admin.site.register(Cat)
admin.site.register(Dog)