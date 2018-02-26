import operator
import calendar

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from .models import Post, Comment, KeyWords
from .forms import PostForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from functools import reduce




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    cal = calendar.calendar(2025,2,1,5)
    return render(request, 'yourblog/post_list.html', {'posts': posts, 'cal': cal, 'keywords': KeyWords.objects.all()})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'yourblog/post_detail.html', {'post': post, 'keywords': KeyWords.objects.all()})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'yourblog/post_edit.html', {'form': form, 'keywords': KeyWords.objects.all()})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'yourblog/post_edit.html', {'form': form, 'keywords': KeyWords.objects.all()})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'yourblog/post_draft_list.html', {'posts': posts, 'keywords': KeyWords.objects.all()})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def publish(self):
    self.published_date = timezone.now()
    self.save()


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'yourblog/add_comment_to_post.html', {'form': form, 'keywords': KeyWords.objects.all()})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def register(request):
    context = {}
    register_form = UserCreationForm()
    template_name = "register.html"
    context = {"register_form": register_form}
    if request.method == "POST":
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2'])
            auth.login(request, new_user)
            return HttpResponseRedirect('/')
        else:
            register_form = new_user_form
            context = {"register_form": register_form}
    return render(request, 'register.html', context)


def keywords(request, pk):
    args = {}

    args['keywords'] = KeyWords.objects.all()
    args['keyw_s'] = KeyWords.objects.get(pk=pk)
    args['posts'] = Post.objects.filter(keywords__name__exact=args['keyw_s'])
    args['username'] = auth.get_user(request).username
    return render(request, 'yourblog/keywpage.html', args)
