from rest_framework import serializers
from django.contrib.auth.models import User
from petflix.models import Pet
from petflix.models import Dog
from petflix.models import Cat
from petflix.models import AdoptionRequest

class PetsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('name', 'original_owner', 'birthdate', 'eyecolor', 'description', 'is_adopted', 'updated_at', 'created_at', 'id', 'pet_type')
        extra_kwargs = {
            'original_owner': {'required': False, 'allow_null': True}
        }

class DogSerializer(PetsModelSerializer):
    class Meta:
        model = Dog
        fields = tuple(PetsModelSerializer.Meta.fields) + tuple(['breed', 'size'])


class CatSerializer(PetsModelSerializer):
    class Meta:
        model = Cat
        fields = tuple(PetsModelSerializer.Meta.fields) + tuple(['breed', 'color']) 

class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Certifica de que a senha é capturada

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        # Cria o usuário normalmente, mas usa set_password para garantir que a senha será hashada
        password = validated_data.pop('password')  # Retira a senha do validated_data
        user = User(**validated_data)  # Cria o usuário sem a senha
        user.set_password(password)  # Agora define a senha, que será hashada
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Verifica se a senha foi passada para atualizar
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Se a senha for fornecida, atualiza
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
    
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = ('request_date', 'status', 'id', 'user_id', 'pet_id')
        extra_kwargs = {
            'user_id': {'required': False},
            'pet_id': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        validated_data['pet_id'] = self.context['pet_id']
        return super().create(validated_data)