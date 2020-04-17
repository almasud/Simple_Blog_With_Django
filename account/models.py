from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from website.utils import profile_directory_path


class UserProfile(models.Model):
    # UserProfile Model Manager
    class UserProfileManager(models.Manager):
        def get_dhaka(self):
            return self.filter(city='Dhaka')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(max_length=200)
    city = models.CharField(max_length=50)
    website = models.URLField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to=profile_directory_path, blank=True, validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', ])])

    objects = UserProfileManager()  # Set default QuerySet.

    # success_url for CreateView and UpdateView
    def get_absolute_url(self):
        return reverse('account:view_profile_with_pk', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username


"""
Django signals allow decoupled applications get notified when actions 
occur elsewhere in the framework. signals allow certain senders to 
notify a set of receivers that some action has taken place.

post_save signal is sent at the end of a model’s save() method.
sender: The model class.
instance: The actual instance being saved.
created: A boolean; True if a new record was created.
"""


# Alternatively, we can use a @receiver() decorator.
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


"""
To receive a signal, register create_profile as a receiver function 
using the post_save.connect() method. The create_profile function is 
called when the post_save signal is sent.
"""
post_save.connect(create_profile, sender=User)  # Listening to signals.
