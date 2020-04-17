from django import forms
from django.contrib.auth.models import User
from . models import UserProfile
from django.contrib.auth.forms import (
	UserCreationForm, UserChangeForm, PasswordChangeForm,
	AuthenticationForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.hashers import check_password
# For Form Validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class UserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 
			'username', 'password1', 'password2',
			)
	
	first_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your first name...',
			})
		)

	last_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your last name...',
			})
		)

	email = forms.EmailField(required=True, 
		help_text='Enter an valid email address.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your email address...',
			})
		)

	username = forms.CharField(required=True, max_length=50, 
		help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your username...',
			})
		)

	password1 = forms.CharField(required=True, min_length=8, label='Password', 
		help_text="<ul><li>Your password can't be too similar to your other personal information.</li>"
			"<li>Your password must contain at least 8 characters.</li>"
			"<li>Your password can't be a commonly used password.</li>"
			"<li>Your password can't be entirely numeric.</li></ul>", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your password...',
			})
		)

	password2 = forms.CharField(required=True, min_length=8, label='Password confirmation', 
		help_text="Enter the same password as before, for verification.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Re-enter your password...',
			})
		)

	def clean_first_name(self):
		f_name = self.cleaned_data['first_name']
		if f_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, f_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return f_name

	def clean_last_name(self):
		l_name = self.cleaned_data['last_name']
		if l_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, l_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return l_name

	def clean_email(self):
		email = self.cleaned_data['email']
		return email


class UserUpdateForm(UserChangeForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 
			'username', 'password', 'confirm_password',
			)

	first_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your first name...',
			})
		)
	last_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your last name...',
			})
		)
	email = forms.EmailField(required=True,  
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your email address...',
			})
		)

	username = forms.CharField(required=True, max_length=50, 
		help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your username...',
			})
		)

	confirm_password = forms.CharField(required=True, label='Confirm your password', 
		help_text="Enter your password to varify it's you.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your password...',
			})
		)

	def clean_first_name(self):
		f_name = self.cleaned_data['first_name']
		if f_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, f_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return f_name

	def clean_last_name(self):
		l_name = self.cleaned_data['last_name']
		if l_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, l_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return l_name

	def clean_email(self):
		email = self.cleaned_data['email']
		return email

	def clean_confirm_password(self):
		confirm_password = self.cleaned_data['confirm_password']
		if confirm_password:
			if not check_password(confirm_password, self.instance.password):
				raise ValidationError(
				    _('Password does not match! Please re-enter your password.')
				)
		return confirm_password


class ProfileUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Set existing image as old_image for later use in view
		self.old_image = self.instance.image

	class Meta:
		model = UserProfile
		fields = ('description', 'city', 'website', 'mobile_number','image',)

	description = forms.CharField(required=False, max_length=200, 
		help_text="Describe about you within 200 characters.", 
		widget=forms.Textarea(attrs={
			'class': 'form-control', 'placeholder': 'Write something about you...',
			'rows': '5',
			}),
		)
	city = forms.CharField(required=False, max_length=50,
		help_text='Enter maximum 50 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your city...',
			})
		)
	website = forms.CharField(required=False, max_length=50, 
		help_text='Enter maximum 50 characters.', 
		widget=forms.URLInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your website...',
			})
		)
	mobile_number = forms.CharField(required=False, max_length=30, 
		help_text='Allow 13 or 11 digits after +88 or 01.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your mobile number...',
			})
		)
	image = forms.FileField(required=False, label='Upload a profile picture', 
		help_text="Allowed extentions: ['jpg', 'jpeg', 'png',]", 
		widget=forms.FileInput(attrs={
			'class': 'form-control-file',
			}),
		)

	def clean_description(self):
		description = self.cleaned_data['description']
		return description

	def clean_city(self):
		city = self.cleaned_data['city']
		return city

	def clean_website(self):
		website = self.cleaned_data['website']
		return website

	def clean_mobile_number(self):
		mobile_number = self.cleaned_data['mobile_number']
		if mobile_number:
			pattern = r'^(?:\+88|01)?(?:\d{11}|\d{13})$'  # Allow 13 or 11 digits after +88 or 01.
			if not re.match(pattern, mobile_number):
				raise ValidationError(
				    _('Invalid mobile number! Please enter a valid mobile number.')
				)
		return mobile_number

	def clean_image(self):
		# image attribute contain old image if not select any new
		image = self.cleaned_data['image']
		return image


class UserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 
			'username', 'password1', 'password2',
			)
	
	first_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your first name...',
			})
		)

	last_name = forms.CharField(required=False, max_length=20, 
		help_text='Enter maximum 20 characters.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your last name...',
			})
		)

	email = forms.EmailField(required=True, 
		help_text='Enter an valid email address.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your email address...',
			})
		)

	username = forms.CharField(required=True, max_length=50, 
		help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', 
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your username...',
			})
		)

	password1 = forms.CharField(required=True, min_length=8, label='Password', 
		help_text="<ul><li>Your password can't be too similar to your other personal information.</li>"
			"<li>Your password must contain at least 8 characters.</li>"
			"<li>Your password can't be a commonly used password.</li>"
			"<li>Your password can't be entirely numeric.</li></ul>", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your password...',
			})
		)

	password2 = forms.CharField(required=True, min_length=8, label='Password confirmation', 
		help_text="Enter the same password as before, for verification.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Re-enter your password...',
			})
		)

	def clean_first_name(self):
		f_name = self.cleaned_data['first_name']
		if f_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, f_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return f_name

	def clean_last_name(self):
		l_name = self.cleaned_data['last_name']
		if l_name:
			pattern = r'^[A-z][A-z|\.|\s]+$'
			if not re.match(pattern, l_name):
				raise ValidationError(
				    _('Invalid name! Please enter a valid name.')
				)
		return l_name

	def clean_email(self):
		email = self.cleaned_data['email']
		return email


class UserLoginForm(AuthenticationForm):

	class Meta:
		model = User
		fields = ( 'username', 'password',)


	username = forms.CharField(required=True, max_length=50,
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your username...',
			})
		)

	password = forms.CharField(required=True,
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your password...',
			})
		)


class UserPasswordResetForm(PasswordResetForm):
	class Meta:
		model = User
		fields = ( 'email',)


	email = forms.EmailField(required=True,  
		widget=forms.TextInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your email...',
			})
		)

	def clean_email(self):
		email = self.cleaned_data['email']
		return email


class UserSetPasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ( 'new_password1', 'new_password2',)


	new_password1 = forms.CharField(required=True, min_length=8, label='New password', 
		help_text="<ul><li>Your password can't be too similar to your other personal information.</li>"
			"<li>Your password must contain at least 8 characters.</li>"
			"<li>Your password can't be a commonly used password.</li>"
			"<li>Your password can't be entirely numeric.</li></ul>", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your new password...',
			})
		)

	new_password2 = forms.CharField(required=True, min_length=8, label='New password confirmation', 
		help_text="Enter the same password as before, for confirmation.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Re-enter your new password...',
			})
		)


class UserPasswordChangeForm(PasswordChangeForm):
	class Meta:
		model = User
		fields = ( 'old_password','new_password1', 'new_password2',)


	old_password = forms.CharField(required=True, min_length=8, label='Old password', 
		help_text="Type your old password to varify it's you.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your old password...',
			})
		)

	new_password1 = forms.CharField(required=True, min_length=8, label='New password', 
		help_text="<ul><li>Your password can't be too similar to your other personal information.</li>"
			"<li>Your password must contain at least 8 characters.</li>"
			"<li>Your password can't be a commonly used password.</li>"
			"<li>Your password can't be entirely numeric.</li></ul>", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Enter your new password...',
			})
		)

	new_password2 = forms.CharField(required=True, min_length=8, label='New password confirmation', 
		help_text="Enter the same password as before, for confirmation.", 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control', 'placeholder': 'Re-enter your new password...',
			})
		)

