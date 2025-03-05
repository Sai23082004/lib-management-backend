from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import *
from users.serializers import *
from users.models import *
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .utils import send_otp_email
from .models import *
from django.contrib.auth.models import User

from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Django Backend is Running!"})

def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})

class Register(APIView):
    def post(self, request):
        # Step 1: Create user
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Step 2: Send OTP email
            otp_instance = send_otp_email(user)

            return Response({
                'message': "User created. Please check your email for OTP to verify your account.",
                'email': user.email,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterVerifyOTP(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid email!"}, status=status.HTTP_400_BAD_REQUEST)

            # Check OTP
            otp_instance = OTP.objects.filter(user=user, otp=otp_code).last()

            if not otp_instance or otp_instance.is_expired():
                return Response({"error": "Invalid or expired OTP!"}, status=status.HTTP_400_BAD_REQUEST)

            # OTP is valid, activate user or complete registration
            user.is_active = True  # You may want to activate the user now
            user.save()

            return Response({"message": "Registration successful, your account is now activated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            otp_code = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Email not found!"}, status=status.HTTP_400_BAD_REQUEST)

            # Check OTP
            otp_instance = OTP.objects.filter(user=user, otp=otp_code).last()
            if not otp_instance or otp_instance.is_expired():
                return Response({"error": "Invalid or expired OTP!"}, status=status.HTTP_400_BAD_REQUEST)

            # Update password
            user.set_password(new_password)
            user.is_active = True
            user.save()

            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Email not found!"}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance = send_otp_email(user)

            return Response({"message": "OTP sent to your email for password reset."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                'user': user.username,
                'refresh': str(refresh),
                'token': access_token,
            }, status=status.HTTP_200_OK)

            # # Set token in HttpOnly cookie
            # response.set_cookie(
            #     key='access_token', 
            #     value=access_token, 
            #     httponly=True, 
            #     secure=True,  # Set True if using HTTPS
            #     samesite='Lax'
            # )

            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        
        # Remove the access_token cookie
        response.delete_cookie('access_token')

        return response


class StudentRegistrations(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetAllBooks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # print(request.user)
        books = BooksModel.objects.filter(library = request.user)
        # books = BooksModel.objects.all()
        serializer = GetBooksSerializer(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = BooksSerializer(data=request.data, context={'request': request})  # Pass request in context
        if serializer.is_valid():
            serializer.save()  # No need to manually set user anymore
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        serializer = BooksSubmitSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid():
            book = serializer.validated_data['book_instance']  # Get validated book instance
            book.submited = True
            book.return_date = datetime.datetime.now()
            book.save()

            return Response({"message": "Book updated successfully"}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.data.get('user')
        book_id = request.data.get('code')

        if not user_id or not book_id:
            return Response({"error": {"user":"username","code":"book_code"}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UsersModel.objects.get(id=user_id)
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found. Please register."}, status=status.HTTP_404_NOT_FOUND)

        try:
            book = BooksModel.objects.get(id=book_id, user=user,)                                    
        except BooksModel.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"success": "Book has been deleted successfully."}, status=status.HTTP_200_OK)

class GetAllStudents(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        users = UsersModel.objects.filter(user=request.user)
        serializer = StudentSerializer(users,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DeleteStudent(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        roll = request.data.get('roll') 
        if not roll:
            return Response({"roll":"roll number required"},status=status.HTTP_400_BAD_REQUEST)
        vendor = request.user
        try:
            user = User.objects.get(username=vendor)
        except User.DoesNotExist:
            return Response({"error":"library not found"},status=status.HTTP_400_BAD_REQUEST)
        try:
            student = UsersModel.objects.get(user=user,roll=roll)  
        except UsersModel.DoesNotExist:
            return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
        student.delete() 
        return Response({"success":"user has been deleted successfully"},status=status.HTTP_200_OK)