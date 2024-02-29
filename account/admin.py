from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from .models import User
# Register your models here.


class UserAdmin(BaseUserAdmin):
	list_display = ['email', 'first_name', 'last_name', 'is_admin', 'is_active']
	list_filter = ['is_admin', 'is_staff', 'is_active']

	fieldsets = [
			(None, {"fields": ['email', 'password']}),
			("Personal info", {"fields": ['first_name', 'last_name']}),
			("Permissions", {'fields': ['is_admin', 'is_staff', 'is_active']}),
	]


	add_fieldsets = [
			(None, {"classes":['wide'],
				"fields":['email', 'first_name', 'last_name', 'password1', 'password2']})
	]


	search_fields = ['email']
	ordering = ['first_name', 'last_name']
	filter_horizontal = []


admin.site.register(User, UserAdmin)