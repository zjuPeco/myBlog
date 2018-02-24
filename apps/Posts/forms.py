# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'

from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [ "title",  "image", "content", "draft", "publish"]