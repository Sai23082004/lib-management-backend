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

class Register(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = RefreshToken.for_user(user)
            return Response({
                'user': user.username,
                'refresh':str(token),
                'token': str(token.access_token),
                },status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': user.username,
                'refresh':str(refresh),
                'token': str(refresh.access_token),
                },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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

