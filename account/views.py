from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import User
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, 
						ChangePasswordSerializer, SendPasswordResetEmailSerializer,
						ResetPasswordSerializer
					)
from .renderers import UserRenderer

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
	renderer_classes = [UserRenderer]
	
	def post(self, request, format=None):
		serializer = UserRegistrationSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			token = get_tokens_for_user(user)
			return Response({'token':token, 'msg':'User is registered successfully.'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(APIView):
	renderer_classes = [UserRenderer]

	def post(self, request, format=None):
		serializer = UserLoginSerializer(data=request.data)
		if serializer.is_valid():
			email = serializer.data.get('email')
			password = serializer.data.get('password')
			user = authenticate(request, email=email, password=password)

			if user is not None:
				login(request, user)
				token = get_tokens_for_user(user)
				return Response({'token':token, 'msg':'You are logged in successfully'}, status=status.HTTP_200_OK)
			else:
				return Response({'errors':{"non_field_errors":"Please enter valid credentials."}}, status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
	renderer_classes = [UserRenderer]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		serializer = UserProfileSerializer(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)
	


class ChangePasswordView(APIView):
	renderer_classes = [UserRenderer]
	permission_classes = [IsAuthenticated]

	def post(self, request, format=None):
		serializer = ChangePasswordSerializer(data=request.data, context={'user':request.user})
		if serializer.is_valid():
			return Response({"msg": "Password changed successfully."}, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendPasswordResetEmailView(APIView):
	renderer_classes = [UserRenderer]

	def post(self, request, format=None):
		serializer = SendPasswordResetEmailSerializer(data=request.data)
		if serializer.is_valid():
			return Response({"msg": "Password changed successfully."}, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(APIView):
	renderer_classes = [UserRenderer]

	def post(self, request, uid, token, format=None):
		serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})

		if serializer.is_valid():
			return Response({'msg':"Password reset successfully."}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)