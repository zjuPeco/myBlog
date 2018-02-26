# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'


from django.urls import path
from .views import *


app_name = 'comments'
urlpatterns = [
    path('<int:id>/', comment_thread, name='comment_thread'),
    path('<int:id>/delete/', comment_delete, name='comment_delete'),
]