from django.contrib import admin
from .models import *
from users.models import *

# Register your models here.
admin.site.register(UsersModel)
admin.site.register(BooksModel)