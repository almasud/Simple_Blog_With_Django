from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import messages
from . import views
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
	UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm,
	UserSetPasswordForm,
)


app_name = 'account'


urlpatterns = [
	path('login/', auth_views.LoginView.as_view(
		authentication_form=UserLoginForm,
		template_name='account/login.html',
		), name='login'
	),
	path('logout/', auth_views.LogoutView.as_view(
		next_page='account:login',
		), name='logout'),
	path('password_change/', auth_views.PasswordChangeView.as_view(
			template_name='account/password_change.html',
			form_class=UserPasswordChangeForm,
			success_url=reverse_lazy('account:password_change_done'),
		), name='password_change'
	),
	path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
			template_name='account/password_change_done.html',	
		), name='password_change_done'
	),
	path('password_reset/', auth_views.PasswordResetView.as_view(
		form_class=UserPasswordResetForm,
		template_name='account/password_reset.html',
		success_url=reverse_lazy('account:password_reset_done'),
		email_template_name='account/password_reset_email.html',
		), 
		name='password_reset'
	),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
		template_name='account/password_reset_done.html'
		), 
		name='password_reset_done'
	),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
		form_class=UserSetPasswordForm,
		template_name='account/password_reset_confirm.html',
		success_url=reverse_lazy('account:password_reset_complete'),
		), 
		name='password_reset_confirm'
	),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
		template_name='account/passowrd_reset_complete.html'
		), 
		name='password_reset_complete'
	),
	path('register/', views.UserCreate.as_view(), name='register'),
	path('<slug:username>/', views.ProfileView.as_view(), name='view_profile'),
	path('profile/edit/', views.update_profile, name='edit_profile'),
]