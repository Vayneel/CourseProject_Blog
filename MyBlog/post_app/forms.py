from django import forms
from post_app.models import *


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rating']


class SearchForm(forms.Form):
    by_name = forms.CharField(max_length=225, required=False)
    by_tag = forms.CharField(max_length=30, required=False)
    by_author = forms.CharField(max_length=191, required=False)
