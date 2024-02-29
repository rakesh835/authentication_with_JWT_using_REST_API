from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from auth_using_JWT_with_restAPI_project import settings

from .models import User




class UserRegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name', 'password', 'password2']
		extra_kwargs = {
				'password':{'write_only':True}
		}


	def validate(self, data):
		password1 = data.get('password')
		password2 = data.get('password2')

		if password1 != password2:
			raise serializers.ValidationError('Passwords do not match.')

		return data

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)



class UserLoginSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(max_length=255, allow_blank=False)
	class Meta:
		model = User
		fields = ['email', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'first_name', 'last_name']


class ChangePasswordSerializer(serializers.Serializer):
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

	class Meta:
		fields = ['password', 'password2']

	def validate(self, data):
		password = data.get('password')
		password2 = data.get('password2')
		user = self.context.get('user')

		if password != password2:
			raise serializers.ValidationError('Passwords do not match.')
		else:
			user.set_password(password)
			user.save()

			return data



class SendPasswordResetEmailSerializer(serializers.Serializer):
	email = serializers.EmailField(max_length=255)

	class Meta:
		fields = ['email',]

	def validate(self, data):
		email = data.get('email')

		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			subject = 'Reset your Password'
			protocol = 'http'
			domain = '127.0.0.1:8000/'
			uid = urlsafe_base64_encode(force_bytes(user.id))
			token = PasswordResetTokenGenerator().make_token(user)
			link = protocol + "://" + domain + "account/user/reset-password/" + uid + "/" + token
			message = "Please click the following link to reset your password:\n" + link
			from_email = settings.EMAIL_HOST_USER
			
			print("link: ", link)

			send_mail(subject, message, from_email, [email,], fail_silently=False,)
			return data
		else:
			raise serializers.ValidationError('You are not a Registered User')



class ResetPasswordSerializer(serializers.Serializer):
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

	class Meta:
		fields = ['password', 'password2']

	def validate(self, data):
		password = data.get('password')
		password2 = data.get('password2')
		uid = self.context.get('uid')
		token = self.context.get('token')

		if password != password2:
			raise serializers.ValidationError('Passwords do not match.')
		else:
			user_id = smart_str(urlsafe_base64_decode(uid))
			user = User.objects.get(id=user_id)

			if PasswordResetTokenGenerator().check_token(user, token):
				user.set_password(password)
				user.save()

				return data
			else:
				raise serializers.ValidationError('Token is either invalid or expired.')
