from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Projects(models.Model):
    project_name = models.CharField(max_length=50, verbose_name='项目名称')
    project_description = models.TextField(verbose_name='项目描述', default='')
    add_date = models.DateTimeField(verbose_name='添加时间', default=datetime.now())
    project_author = models.CharField(max_length=50, verbose_name='项目作者')
    image = models.ImageField(upload_to='project_img/%Y/%m', verbose_name='项目封面', max_length=100, default='project_img/default.jpg')
    url = models.URLField(max_length=200, verbose_name='访问地址', default='')
    github_url = models.URLField(max_length=200, verbose_name='github地址', default='')

    def __str__(self):
        return self.project_name

    class Meta():
        verbose_name = '项目管理'
        verbose_name_plural = verbose_name

