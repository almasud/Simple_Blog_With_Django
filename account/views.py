from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import RedirectView
from .forms import (
    UserForm, UserUpdateForm, ProfileUpdateForm,
)
# from django.contrib.auth import update_session_auth_hash  # For stay login
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from website.utils import login_required
from .models import UserProfile
import os


# Message for log out
def logout_message(request, **kwargs):
    html_output = """<p>Hey, You have successfully logged out.
	Thanks for spending some quality time with the Web site today.
	<a href=""" + str(reverse_lazy('account:login')) + """>Log in again</a></p>"""
    messages.info(request, html_output)


user_logged_out.connect(logout_message)


# Message for log in
def login_message(request, **kwargs):
    html_output = """<p>Welcome """ + request.user.username + """! You have successfully logged in. 
	Go to your <a href=""" + str(reverse_lazy('account:view_profile', kwargs={'username': request.user})) + """>Profile</a>.</p>"""
    messages.info(request, html_output)


user_logged_in.connect(login_message)


# This class is used to create user account
class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'account/user_form.html'

    # Success url for create and update view.
    def get_success_url(self):
        return reverse_lazy('blog:post_view')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Congratulations !\nYou have successfully registered.\nNow you can <a href="' +
                         str(reverse_lazy('account:login')) + '">Log in</a> to access your account')
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = None
        messages.error(
            self.request, 'Invalid form submission !\nPlease correct the error in below.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # This method accepts a request argument plus arguments, and
    # returns a HTTP response.
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 'Invalid request !\nYou have already registered.')
            return redirect('account:view_profile', username=self.request.user)
        return super().dispatch(*args, **kwargs)


# This class is used to view user profile
class ProfileView(TemplateView):
    template_name = 'account/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs:
            # We can use get_object_or_404() instead of try case.
            try:
                context['user'] = User.objects.get(username=kwargs['username'])
            except:
                context['user'] = None
                messages.error(self.request, 'Opps!\nUser is not found.')
        return context

    # Decorate every instance of the class.
    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to view any profile."))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# This function is used to update user profile
@login_required(login_url='account:login', message="Sorry!\nYou must login to update any profile.")
def update_profile(request, **kwargs):

    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if request.FILES:
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            # Valid state
            # image attribute contain old image if not select any new
            new_image = request.FILES.get('image')  # New image
            old_image = profile_form.old_image  # Get old image from form
            image_remove_checked = bool(request.POST.get('remove_checked'))
            # Remove image if checked clear
            if image_remove_checked:
                if os.path.isfile(profile.image.path):
                    os.remove(profile.image.path)
                    profile.image = None
            # Remove old image if upload new one
            if new_image:
                if old_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
            user_form.save()
            profile_form.save()
            return redirect('account:view_profile', username=request.user)
        else:
            # Invalid state
            messages.error(
                request, 'Invalid form submission !\nPlease correct the error in below.')
            args = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'account/userprofile_update_form.html', args)
    else:
        # GET state
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        args = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'account/userprofile_update_form.html', args)
