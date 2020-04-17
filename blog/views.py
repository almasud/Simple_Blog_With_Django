from django.shortcuts import (
    render, get_object_or_404, redirect
)
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormMixin
)
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from .forms import PostForm, LoginForm, CommentForm
from website.utils import login_required
import os
from django.contrib.auth.models import User


# This class describes all published posts of all users
class PostList(ListView):
    model = Post
    paginate_by = 5
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(published__lte=timezone.now())


# This class shows all draft post
class PublishedPostList(ListView):
    model = Post
    paginate_by = 5

    context_object_name = "published_posts"

    def get_queryset(self):
        return Post.objects.filter(published__isnull=False, author=self.request.user).order_by('-published')

    # Decorate every instance of the class.
    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to view your published posts."))
    # This method accepts a request and returns a HTTP response.
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# This class shows all draft post
class DraftPostList(ListView):
    model = Post
    paginate_by = 5

    context_object_name = "draft_posts"

    def get_queryset(self):
        return Post.objects.filter(published__isnull=True, author=self.request.user).order_by('-created')

    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to view your draft posts."))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# This class publish a draft post
class PostPublish(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.published = timezone.now()
        post.save()
        self.url = post.get_absolute_url()
        return super().get_redirect_url(*args, **kwargs)


# This class approves a post comment
class ApprovedComment(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        post = Post.objects.get(id=kwargs['post_pk'])
        self.url = post.get_absolute_url()

        if self.request.user == post.author:
            comment.approve()
            messages.success(self.request, 'Comment is approved!')
            return super().get_redirect_url(*args, **kwargs)
        else:
            messages.error(
                self.request, 'Sorry! You have not permission.\nOnly post author can approve this comment.')
            return super().get_redirect_url(*args, **kwargs)


# This class removes a comment
class RemoveComment(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        post = Post.objects.get(id=kwargs['post_pk'])
        self.url = post.get_absolute_url()

        if self.request.user == post.author or self.request.user == comment.author:
            comment.delete()
            messages.success(self.request, 'Comment is removed.')
            return super().get_redirect_url(*args, **kwargs)
        else:
            messages.error(
                self.request, 'Sorry! You have not permission to remove this comment.')
            return super().get_redirect_url(*args, **kwargs)


"""
We can inherit only one generic view - that is, only one parent 
class may inherit from View and the rest (if any) should be mixins.
(Mixins are a form of multiple inheritance where behaviors and 
attributes of multiple parent classes can be combined and are an 
excellent way of reusing code across multiple classes.)
"""


# This class is used to show the details of a post and
# write a comment in those post.
class DetailsPostView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_details.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    # A dictionary used as a template context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user.username
        form.save()
        messages.success(
            self.request, 'Comment successful!\nYour comment will display after approved.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Comment submission is invalid!\nPlease correct the error in below.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        post = get_object_or_404(Post, pk=self.object.pk)
        # For unpublished post.
        if post.published is None:
            if not self.request.user.is_authenticated:
                messages.error(
                    self.request, "Sorry!\nYou must login to view any draft post.")
                return redirect('account:login')
            # For except author
            if not self.request.user == post.author:
                messages.error(
                    self.request, "Sorry!\nYou have not permission to view this post.")
                return redirect('blog:post_view')
        # For published post.
        return super().dispatch(*args, **kwargs)


# This class is used to create a post
class PostCreate(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        if self.request.POST.get('submit') == "publish":
            post.published = timezone.now()
        post.save()
        messages.success(self.request, 'Post successfully added.')
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = None
        messages.error(
            self.request, 'Invalid form submission !\nPlease correct the error in below.')
        return super().form_invalid(form)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Decorate every instance of the class.
    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to add any post."))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# This class is used to update a post
class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        post = form.save(commit=False)
        # photo attribute contain old image if not select any new
        new_photo = self.request.FILES.get('photo')  # New photo
        old_photo = form.old_photo  # Get old photo from form
        photo_remove_checked = bool(self.request.POST.get('remove_checked'))
        # Remove photo if checked clear
        if photo_remove_checked:
            if os.path.isfile(post.photo.path):
                os.remove(post.photo.path)
                post.photo = None
        # Remove old photo if upload new one
        if new_photo:
            if old_photo:
                if os.path.isfile(old_photo.path):
                    os.remove(old_photo.path)
        form.save()
        messages.success(self.request, 'Post successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Invalid form submission !\nPlease correct the error in below.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Decorate every instance of the class.
    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to update any post."))
    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            return super().dispatch(*args, **kwargs)
        else:
            messages.error(
                self.request, 'Sorry! You have not permission.\nOnly author can edit this post.')
            return HttpResponseRedirect(self.object.get_absolute_url())


# This class is used to remove a post
class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/post_details.html'

    def get_success_url(self):
        messages.success(self.request, 'Post deleted successfully.')
        return reverse_lazy('blog:post_view')

    def delete(self, request, *args, **kwargs):
        if self.object.author == request.user:
            self.object.delete()
            if self.object.photo:
                if os.path.isfile(self.object.photo.path):
                    os.remove(self.object.photo.path)
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(
                self.request, 'Sorry! You have not permission.\nOnly author can delete this post.')
            return HttpResponseRedirect(self.object.get_absolute_url())

    # Decorate every instance of the class.
    @method_decorator(login_required(login_url='account:login', message="Sorry!\nYou must login to delete any post."))
    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(*args, **kwargs)
