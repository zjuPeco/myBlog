# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'

from django.urls import path
from django.views.generic import TemplateView
from .views import indexPage

app_name = 'blog'
urlpatterns = [
    path('', indexPage.as_view(), name='index'),
]