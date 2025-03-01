from django.urls import path 
from  .views import *

urlpatterns = [
    path('getbooks/<str:vendor>/<str:id>/', GetBooks.as_view())
]
