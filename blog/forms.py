from django import forms
from .models import Post, Comment
# For Form Validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
# From python
from datetime import datetime
from datetime import timedelta


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set existing photo as old_photo for later use in view
        self.old_photo = self.instance.photo

    class Meta:
        model = Post
        fields = ('title', 'text', 'photo',)

    title = forms.CharField(required=True, max_length=30,
                            help_text='Enter maximum 30 characters.',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control', 'placeholder': 'Enter a post title...',
                            })
                            )

    text = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={
                               'class': 'form-control', 'placeholder': 'Write something...',
                           }),
                           )

    photo = forms.FileField(required=False, label='Upload a photo',
                            help_text="Allowed extentions: ['jpg', 'jpeg', 'png']",
                            widget=forms.FileInput(attrs={
                                'class': 'form-control-file',
                            }),
                            )

    def clean_title(self):
        title = self.cleaned_data['title']
        pattern = r'^[A-Za-z]'
        if not re.match(pattern, title):
            raise ValidationError(
                _('Title cannot start with number!')
            )
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def clean_photo(self):
        # photo attribute contain old image if not select any new
        photo = self.cleaned_data['photo']
        return photo


class LoginForm(forms.Form):

    username = forms.CharField(label="Username", required=True, max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control', 'placeholder': 'Enter Username',
                               }),
                               )

    password = forms.CharField(label="Password", required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control', 'placeholder': 'Enter Password',
                               }),
                               )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    text = forms.CharField(required=True, label='Comment',
                           widget=forms.Textarea(attrs={
                               'class': 'form-control', 'rows': '5',
                               'placeholder': 'Write something about this post...',
                           }),
                           )

    def clean_text(self):
        text = self.cleaned_data['text']
        return text
