from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.core.validators import FileExtensionValidator
from time import strftime
import os
from website.utils import post_directory_path


# Model for user post
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    photo = models.FileField(upload_to=post_directory_path, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', ])])
    created = models.DateTimeField(editable=False, default=timezone.now)
    published = models.DateTimeField(editable=False, blank=True, null=True)

    class Meta:
        ordering = ['-published']

    # success_url for CreateView and UpdateView
    def get_absolute_url(self):
        return reverse_lazy('blog:post_details_view', kwargs={'slug': self.slug, 'year': self.created.strftime('%Y'), 'month': self.created.strftime('%m'), 'day': self.created.strftime('%d')})

    # Return Post object as a string
    def __str__(self):
        return self.title


# Create slug url using post title
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    query_set = Post.objects.filter(slug=slug).order_by('-id')
    if query_set.exists():
        new_slug = '%s-%s' % (slug, query_set.first().id)
        return create_slug(instance, new_slug)
    return slug


# This receiver function called by pre_save signal of Post.
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# This pre_save signal work befor saving a Post.
pre_save.connect(pre_save_post_receiver, sender=Post)


# Model for post comment
class Comment(models.Model):
    # Create a Subclass of Manager to get total number of approved comments.
    class CommentManager(models.Manager):
        def approved_comment_count(self):
            return self.filter(approved_comment=True).count()

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE,
                             related_name='comments')
    author = models.CharField(max_length=30)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    objects = CommentManager()  # Set CommentManager as default.

    class Meta:
        ordering = ['-created']

    # Approve post comment
    def approve(self):
        self.approved_comment = True
        self.save()

    # Return Comment object as a string
    def __str__(self):
        return self.text
