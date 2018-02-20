# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'

from django.urls import path
from .views import *

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('<int:detail_id>/', post_detail, name='post_detail'),
    path('update/', post_update, name='post_update'),
    path('delete/', post_delete, name='post_delete'),
]