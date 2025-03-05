from django.urls import path
from .views import *

urlpatterns = [
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('addbook/',AddBookView.as_view()),
    path('studentregister/',StudentRegistrations.as_view()),
    path('books/',GetAllBooks.as_view()),
    path('allstudents/',GetAllStudents.as_view()),
    path('student/delete/',DeleteStudent.as_view()),
    path('logout/', Logout.as_view(), name='logout'),
    path('get-csrf/', get_csrf_token),  # CSRF Token API
    path('register/verify-otp/', RegisterVerifyOTP.as_view(), name='register_verify_otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
]