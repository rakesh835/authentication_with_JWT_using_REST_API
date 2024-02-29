from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError




class UserManager(BaseUserManager):

	def create_user(self, email, first_name, last_name=None, password=None, password2=None):

		if not email:
			raise ValuError('User must provide a valid email.')

		user = self.model(
						email = self.normalize_email(email),
						first_name = first_name,
						last_name = last_name,
			)

		user.set_password(password)
		user.save(using=self._db)

		return user


	def create_superuser(self, email, first_name, last_name=None, password=None):

		user = self.create_user(email, first_name, last_name, password)
		user.is_admin = True
		user.is_staff = True
		user.is_active = True

		user.save(using=self._db)

		return user



class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255, blank=True, null=True)

	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name']


	def __str__(self):
		return self.email


	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

