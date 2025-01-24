from rest_framework import serializers
from django.contrib.auth.models import User
from petflix.models import Pet

class PetsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('name', 'birthdate', 'eyecolor', 'description', 'original_owner', 'is_adopted', 'updated_at', 'created_at', 'id')

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Update the user instance with validated data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance