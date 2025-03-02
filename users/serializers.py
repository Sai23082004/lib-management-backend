from .models import *
from rest_framework import serializers
import datetime

class StudentSerializer(serializers.ModelSerializer):
    roll = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    branch = serializers.CharField(required=True)
    startyear = serializers.IntegerField(required=True)
    endyear = serializers.IntegerField(required=True)
    gender = serializers.CharField(required=True)

    class Meta:
        model = UsersModel
        fields = '__all__'
        read_only_fields = ['user']  # Prevent user from being manually set

    def validate_email(self, value):
        """
        Check if email is unique before creating a new user.
        """
        if UsersModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        """
        Additional custom validation.
        """
        request = self.context.get('request')  # Get request from serializer context
        if not request or not request.user:
            raise serializers.ValidationError({"user": "Authentication required."})
        user = request.user
        roll = data.get('roll')
        if UsersModel.objects.filter(user=user,roll=roll).exists():
            raise serializers.ValidationError({"roll": "rollNo or username already exists!"})
        
        if data.get('startyear') and data.get('endyear'):
            if data['startyear'] > data['endyear']:
                raise serializers.ValidationError({"startyear": "Start year cannot be greater than end year."})

        return data

    def create(self, validated_data):
        """
        Override create() to automatically assign `user` from request.
        """
        request = self.context.get('request')  # Get request context
        if not request or not request.user:
            raise serializers.ValidationError({"user": "Authentication required."})

        validated_data['user'] = request.user  # Automatically assign logged-in user
        return UsersModel.objects.create(**validated_data)



class BooksSerializer(serializers.ModelSerializer):
    submited_date = serializers.DateField(
        required=True,
        format="%Y-%m-%d",  # Output format
        input_formats=["%Y-%m-%d", "%d-%m-%Y"]  # Accepted input formats
    )
    code = serializers.CharField(required=True)
    user = serializers.CharField(required=True)
    
    class Meta:
        model = BooksModel
        fields = ['user', 'name', 'library', 'code', 'submited_date', 'id']
        extra_kwargs = {'user': {'read_only': True}}  # Prevents users from passing user manually

    def validate(self, data):
        request = self.context.get('request')  # Get request from serializer context
        if not request or not request.user:
            raise serializers.ValidationError({"user": "Authentication required."})

        # Get authenticated user
        user = request.user  
        roll = data.get('user')
        # Get the associated UsersModel instance
        try:
            users_model_instance = UsersModel.objects.get(user=user,roll = roll)
        except UsersModel.DoesNotExist:
            raise serializers.ValidationError({"user": "User does not exist. Please register."})

        # data['user'] = users_model_instance  # Assign user instance
        data['library'] = user
        data['user'] = users_model_instance
        return data

    def create(self, validated_data):
        return BooksModel.objects.create(**validated_data)

        
class GetBooksSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = BooksModel
        fields = '__all__'  # Includes all fields from BooksModel + new custom fields
        extra_fields = ['username', 'branch', 'year']  # Ensure extra fields are added

    def get_username(self, obj):
        return obj.user.firstName if obj.user else None

    def get_branch(self, obj):
        return obj.user.branch if obj.user else None

    def get_year(self, obj):
        return obj.user.startyear if obj.user else None

class BooksSubmitSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)  # Ensure code is required
    id = serializers.IntegerField(required=True)
    # user = serializers.CharField(required=True)
    class Meta:
        model = BooksModel
        fields = ['code','id']  # Removed 'user' and 'id' (handled internally)

    def validate(self, data):
        # request = self.context.get('request')  # Get authenticated user
        # if not request or not request.user:
        #     raise serializers.ValidationError({"user": "Authentication required."})

        # user = request.user
        # try:

        # roll = data.get('user')
        # try:
        #     user_instance = UsersModel.objects.get(user=user,roll=roll)
        # except UsersModel.DoesNotExist:
        #     raise serializers.ValidationError({"user": "User does not exist in the system."})

        code = data.get('code')
        id = data.get('id')

        try:
            book = BooksModel.objects.get(id=id, code=code)
        except BooksModel.DoesNotExist:
            raise serializers.ValidationError({"book": "Book does not exist or does not belong to this user."})

        # data['user'] = user_instance  # Store user instance
        data['book_instance'] = book  # Store book instance for use in view
        return data