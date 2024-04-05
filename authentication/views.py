from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import pyotp
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from Backend_Shop.utils import generate_response_messages
from user.serializers import CustomUserSerializer
from .serializers import RegistrationSerializer
from .models import CustomUser
from django.utils import timezone
from django.conf import settings


def send_otp_code_to_email(email, otp_code):
    subject = 'Maleno Signup'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        # Handle email sending failure
        return False


def generateAndEmailOTP(user, successAction, failureAction):
    # Generate a TOTP secret
    totp_secret = pyotp.random_base32()

    # Set otp_secret to totp_secret and otp_sent_time to current timestamp
    otp_sent_time = timezone.now()
    user.otp_secret = totp_secret
    user.otp_sent_time = otp_sent_time
    user.save()

    # Generate a TOTP code for email
    totp = pyotp.TOTP(totp_secret)
    otp_code_email = totp.now()
    print(otp_code_email, ": OTP")
    emailIsSentSuccessfully = send_otp_code_to_email(user.email, otp_code_email)
    # Send OTP code to user's email
    if emailIsSentSuccessfully:
        return successAction()
    else:
        # Handle failure to send OTP code
        return failureAction()


def registeredSuccessfully(user):
    # Generate a JWT token for the user
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    return Response(
        {
            "data": {"user": {"email": user.email}},
            "token": {"access_token": token},
            **generate_response_messages("User registered successfully. Check your email for OTP code.")
        },
        status=status.HTTP_201_CREATED)


def registeredFailed(user):
    user.delete()
    return Response(generate_response_messages("Failed to register."),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registers user to the server. Input should be in the format:
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(validated_data=serializer.validated_data)
        return generateAndEmailOTP(user, lambda: registeredSuccessfully(user), lambda: registeredFailed(user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Registers user to the server. Input should be in the format:
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, username=email, password=password)
    print(user, email, password)
    if user is not None:
        # User is authenticated, generate token
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        # Serialize user object
        serializer = CustomUserSerializer(user)

        return Response({
            "data": serializer.data,
            "token": {"access_token": token},
            **generate_response_messages("User logged in successfully.")

        }, status=status.HTTP_200_OK)
    else:
        # Invalid credentials
        return Response(generate_response_messages("Invalid email or password."), status=status.HTTP_401_UNAUTHORIZED)


def resendOtpSuccessfully():
    return Response(
        generate_response_messages("OTP resend successfully. Check your email for OTP code."),
        status=status.HTTP_200_OK)


def resendOtpFailed():
    return Response(generate_response_messages("Failed to resend OTP."),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resendOtp(request):
    email = request.data.get('email')
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(generate_response_messages("User not found."), status=status.HTTP_404_NOT_FOUND)
    return generateAndEmailOTP(user, resendOtpSuccessfully, resendOtpFailed)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp_code')

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(generate_response_messages("User not found."), status=status.HTTP_404_NOT_FOUND)

    # Ensure OTP secret is present
    if not user.otp_secret:
        return Response(generate_response_messages("User does not have an OTP secret."),
                        status=status.HTTP_400_BAD_REQUEST)

    # Generate TOTP based on the secret
    totp = pyotp.TOTP(user.otp_secret)
    # print(totp.now(), "DDD")
    # Verify OTP code
    if totp.verify(otp_code):
        # Check if OTP code has expired
        if (timezone.now() - user.otp_sent_time) > timedelta(minutes=settings.OTP_EXPIRATION_TIME):
            return Response(generate_response_messages("OTP code has expired."), status=status.HTTP_400_BAD_REQUEST)

        # OTP code is valid and within the expiration period
        # Perform any additional actions here (e.g., marking user as verified)
        user.signup_confirmed = True
        user.save()

        # Serialize user object
        serializer = CustomUserSerializer(user)
        return Response(
            {
                "data": serializer.data,
                **generate_response_messages("User is verified successfully.")

            }, status=status.HTTP_200_OK)
    else:
        # Invalid OTP code
        return Response(generate_response_messages("Invalid OTP code."), status=status.HTTP_400_BAD_REQUEST)