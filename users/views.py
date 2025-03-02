from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework.status import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class GetBooks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        vendor = request.user
        # print(request.user)
        if not id:
            return Response({"error": "User Id is required"}, status=HTTP_400_BAD_REQUEST)
        # if not vendor:
            # return Response({"error": "library name is required"}, status=HTTP_400_BAD_REQUEST)
        try:
            library = User.objects.get(username=vendor)
        except User.DoesNotExist:
            return Response({"error": "invalid library username"}, status=HTTP_400_BAD_REQUEST)
        # print(library,library.id)
        try:
            user = UsersModel.objects.get(roll=id,user=library)  # Ensure ID is a string
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found, please register"}, status=HTTP_404_NOT_FOUND)

        # Get user details manually
        user_data = {
            "id": user.roll,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone,
            "branch": user.branch,
            "startyear": user.startyear,
            "endyear": user.endyear,
            "gender": user.gender,
            "created": user.created.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        }

        # Get books related to user
        books = BooksModel.objects.filter(library=library,user=user).values(
            "id", "name","code", "created_at", "submited", "return_date", "submited_date"
        )
        books_list = list(books)  # Convert queryset to list of dictionaries

        # Add books to user data
        user_data["books"] = books_list

        return Response(user_data, status=HTTP_200_OK)


class GetUserDetails(APIView):
    def get(self, request, *args, **kwargs):
        vendor = kwargs.get('username')
        id =  kwargs.get('id')
        # print(request.user)
        if not id:
            return Response({"error": "User Id is required"}, status=HTTP_400_BAD_REQUEST)
        # if not vendor:
            # return Response({"error": "library name is required"}, status=HTTP_400_BAD_REQUEST)
        try:
            library = User.objects.get(username=vendor)
        except User.DoesNotExist:
            return Response({"error": "invalid library username"}, status=HTTP_400_BAD_REQUEST)
        # print(library,library.id,id)
        try:
            user = UsersModel.objects.get(user=library,roll=id)  # Ensure ID is a string
        except UsersModel.DoesNotExist:
            return Response({"error": "User not found!"}, status=HTTP_404_NOT_FOUND)

        # Get user details manually
        user_data = {
            "id": user.roll,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone,
            "branch": user.branch,
            "startyear": user.startyear,
            "endyear": user.endyear,
            "gender": user.gender,
            "library":vendor,
            "created": user.created.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        }

        # Get books related to user
        books = BooksModel.objects.filter(library=library,user=user).values(
            "id", "name","code", "created_at", "submited", "return_date", "submited_date"
        )
        books_list = list(books)  # Convert queryset to list of dictionaries

        # Add books to user data
        user_data["books"] = books_list

        return Response(user_data, status=HTTP_200_OK)