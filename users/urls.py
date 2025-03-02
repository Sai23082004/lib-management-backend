from django.urls import path 
from  .views import *

urlpatterns = [
    path('getbooks/<str:id>/', GetBooks.as_view()),
    path('getuserdetails/<str:username>/<str:id>/',GetUserDetails.as_view()),
]
