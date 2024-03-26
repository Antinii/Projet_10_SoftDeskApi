from rest_framework import serializers
from authentication.models import User
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
          model = User
          fields =  ['id', 'username', 'email', 'birthdate', 'can_be_contacted', 'can_data_be_shared'] 
    

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'birthdate', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
            
    def validate_birthdate(self, value):
        """
        Validate that the user is at least 15 years old.
        """
        today = datetime.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < 15:
            raise serializers.ValidationError("Users must be at least 15 years old to create an account.")
        
        return value
