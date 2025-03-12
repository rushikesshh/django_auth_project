from django.shortcuts import render

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
import random

User = get_user_model()

# Temporary store for OTPs (Should use DB or Cache in production)
otp_storage = {}

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        username = request.data.get("username")

        if not email or not password or not username:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
        otp_storage[email] = otp  # Store OTP temporarily

        # Send OTP (In production, use Email API)
        print(f"OTP for {email}: {otp}")

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)


class VerifyRegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")
        username = request.data.get("username")

        if otp_storage.get(email) == otp:
            user = User.objects.create_user(email=email, username=username, password=password)
            del otp_storage[email]  # Remove OTP after successful verification
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "username": user.username
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({"message": "Logged out successfully"})
    response.delete_cookie('auth_token')  # Delete the cookie
    return response
