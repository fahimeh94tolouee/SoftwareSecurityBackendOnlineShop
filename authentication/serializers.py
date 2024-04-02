from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from Backend_Shop.utils import generate_response_messages, validate_password

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        if not email:
            raise serializers.ValidationError(generate_response_messages("Email cannot be empty."))

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError(generate_response_messages("Invalid email format."))

        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            if existing_user.signup_confirmed:
                raise serializers.ValidationError(generate_response_messages("Email is already registered."))

        password = data.get('password')
        validate_password(password)

        return data

    def create(self, validated_data):
        email = validated_data['email']
        existing_user = User.objects.filter(email=email).first()
        if existing_user and not existing_user.signup_confirmed:
            return existing_user
        user = User.objects.create_user(
            username= validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            signup_confirmed=False,
        )
        return user
