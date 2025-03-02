from rest_framework.serializers import Serializer,ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

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
            password=validated_data['password'],
        )
        user.is_active = False  # Set the user as inactive by default
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=8)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email!"})  # More specific error message
        if user.is_active == False:
            raise serializers.ValidationError({"email": "please activate your account! for that click forgot password"})  # More specific error message
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid password!"})

        return {'user': user}  # Return user only if authentication is successful
    
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email!"})

        # Check if OTP exists for this user
        otp_instance = OTP.objects.filter(user=user, otp=otp_code).last()

        if not otp_instance:
            raise serializers.ValidationError({"otp": "Invalid OTP!"})

        if otp_instance.is_expired():
            raise serializers.ValidationError({"otp": "OTP has expired!"})

        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.EmailField()