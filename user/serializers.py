from rest_framework import serializers
from authentication.models import CustomUser
from Backend_Shop.utils import validate_password, generate_response_messages


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'postal_code', 'phone_number', 'credit_card']

    def validate(self, data):
        email = data.get('email')
        if not email:
            raise serializers.ValidationError(generate_response_messages("Email cannot be empty."))
        first_name = data.get('first_name')
        if not first_name:
            raise serializers.ValidationError(generate_response_messages("First Name cannot be empty."))
        last_name = data.get('last_name')
        if not last_name:
            raise serializers.ValidationError(generate_response_messages("Last Name cannot be empty."))
        address = data.get('address')
        if not address:
            raise serializers.ValidationError(generate_response_messages("Address cannot be empty."))
        postal_code = data.get('postal_code')
        if not postal_code:
            raise serializers.ValidationError(generate_response_messages("Postal Code cannot be empty."))
        phone_number = data.get('phone_number')
        if not phone_number:
            raise serializers.ValidationError(generate_response_messages("Phone Number cannot be empty."))
        credit_card = data.get('credit_card')
        if not credit_card:
            raise serializers.ValidationError(generate_response_messages("Credit card cannot be empty."))
        return data

class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
