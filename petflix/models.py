from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

# Pets > Dogs & Cats
class Pet(models.Model):
    EYE_COLORS = [
        ('brown', 'Brown'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('gray', 'Gray'),
        ('heterochromia', 'Heterochromia'),
    ]

    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'), 
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    birthdate = models.DateField()
    eyecolor = models.CharField(max_length=20, choices=EYE_COLORS, default='brown')
    description = models.TextField(max_length=200)
    original_owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    is_adopted = models.BooleanField(default=False)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES, default='dog')
    #slug = models.SlugField(max_length=30, unique=True)

    def age(self):
        return timezone.now().year - self.birthdate.year

    def __str__(self):
        return self.name

# Proxy Model
class PetAdoption(Pet):
    class Meta:
        proxy = True
        ordering = ['created_at']

    def time_waiting(self):
        return timezone.now() - self.created_at

class Dog(Pet):
    BREEDS = [
        ('labrador', 'Labrador'),
        ('beagle', 'Beagle'),
        ('bulldog', 'Bulldog'),
        ('poodle', 'Poodle'),
        ('germanshepherd', 'German Shepherd'),
        ('goldenretriever', 'Golden Retriever'),
        ('undefined', 'Undefined'),
    ]
    SIZES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('undefined', 'Undefined'),
    ]
    breed = models.CharField(max_length=20, choices=BREEDS, default='undefined')
    size = models.CharField(max_length=20, choices=SIZES, default='undefined')

class Cat(Pet):
    BREEDS = [
        ('persian', 'Persian'),
        ('siamese', 'Siamese'),
        ('mainecoon', 'Maine Coon'),
        ('ragdoll', 'Ragdoll'),
        ('bengal', 'Bengal'),
        ('sphynx', 'Sphynx'),
        ('undefined', 'Undefined'),
    ]
    COLORS = [
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('orange', 'Orange'),
        ('brown', 'Brown'),
        ('multi', 'Multi'),
        ('undefined', 'Undefined'),
    ]
    breed = models.CharField(max_length=20, choices=BREEDS, default='undefined')
    color = models.CharField(max_length=20, choices=COLORS, default='undefined')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    birth_date = models.DateField()
    telephone = models.CharField(max_length=15)

class AdoptionRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Adoption request by {self.user.first_name} for {self.pet.name}"