from rest_framework import serializers


def generate_response_messages(error_messages):
    if not isinstance(error_messages, list):
        error_messages = [error_messages]
    return {"message": error_messages}


def convert_dict_to_array(dictionary):
    """
    Convert a dictionary to an array of strings.
    """
    array = []
    for field, values in dictionary.items():
        array.extend(values)
    return array


def validate_password(password):
    if not password:
        raise serializers.ValidationError(generate_response_messages("Password cannot be empty."))
    if len(password) < 8:
        raise serializers.ValidationError(generate_response_messages("Password must be at least 8 characters long."))
    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        raise serializers.ValidationError(
            generate_response_messages("Password must contain both uppercase and lowercase letters."))
    if not any(char.isdigit() for char in password):
        raise serializers.ValidationError(generate_response_messages("Password must contain digits."))
    special_characters = "!@#$%^&*()_+[]{}?:;|'\"<>,./"
    if not any(char in special_characters for char in password):
        raise serializers.ValidationError(generate_response_messages("Password must contain special characters."))
