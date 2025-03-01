from rest_framework.serializers import Serializer,ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True,max_length=8)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id','username','email','password'] 
        
    def validate(self,data):
        email = data['email']
        username = data['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists!")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email already exists!")
        return data
            
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,max_length=8)
    
    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is  None:
            raise serializers.ValidationError("invalid user name or password")
        return {'user': user} 