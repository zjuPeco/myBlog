# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ "title", "content"]