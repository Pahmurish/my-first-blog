from django import forms

from .models import Post, Comment
from django.contrib.admin.widgets import AdminDateWidget




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'keywords')




class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)




