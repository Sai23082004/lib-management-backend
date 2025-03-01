from django.urls import path
from .views import *

urlpatterns = [
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('addbook/',AddBookView.as_view()),
    path('studentregister/',StudentRegistrations.as_view()),
    path('books/',GetAllBooks.as_view()),
    path('allstudents/',GetAllStudents.as_view()),
    
]