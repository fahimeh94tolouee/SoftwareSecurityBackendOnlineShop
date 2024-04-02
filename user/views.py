from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Backend_Shop.utils import generate_response_messages, convert_dict_to_array
from user.serializers import CustomUserSerializer, CheckPasswordSerializer


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getInfo(request):
    """
    Get user information.
    """
    user = request.user

    # Serialize user object
    serializer = CustomUserSerializer(user)

    return Response({
        "data": serializer.data,
        **generate_response_messages("Get user info successfully.")
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    """
    Change user password.
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # Validate old password
    if not user.check_password(old_password):
        return Response(generate_response_messages("Incorrect old password."), status=status.HTTP_400_BAD_REQUEST)

    # Validate new password and confirmation
    serializer = CheckPasswordSerializer(data={"password": new_password})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check if new password meets strength requirements
    if new_password != confirm_password:
        return Response(generate_response_messages("New password and confirmation do not match."), status=status.HTTP_400_BAD_REQUEST)

    # Update user password
    user.set_password(new_password)
    user.save()

    return Response(generate_response_messages("Password changed successfully."), status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def updateInfo(request):
    user = request.user

    serializer = CustomUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {"data": serializer.data, **generate_response_messages("Personal information updated successfully.")}
        return Response(data)
    else:
        error_messages = convert_dict_to_array(serializer.errors)
        error_messages = generate_response_messages(error_messages)
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)