from django.db import models
from django.contrib.auth.models import User


class UsersModel(models.Model):
    user = models.ForeignKey(User, related_name="students", on_delete=models.CASCADE, null=True, blank=True)  # TEMP fix
    roll = models.CharField(max_length=20, blank=True, null=True)
    firstName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)  
    phone = models.CharField(max_length=15, blank=True)  
    created = models.DateTimeField(auto_now_add=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    startyear = models.IntegerField(null=True, blank=True)
    endyear = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.roll}"


class BooksModel(models.Model):
    library = models.ForeignKey(User,null=True,blank=True,related_name="library_books",on_delete=models.CASCADE)
    user = models.ForeignKey(UsersModel, related_name="books", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=40,null=True,blank=True)  # Ensure primary_key=True
    created_at = models.DateTimeField(auto_now_add=True)
    submited = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    submited_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
