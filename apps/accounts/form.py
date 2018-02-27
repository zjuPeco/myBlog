# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'


from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("用户或密码错误")
            if not user.is_active:
                raise forms.ValidationError("用户已禁用")
        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='邮箱地址')
    email2 = forms.EmailField(label='邮箱地址确认')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password', 'password2']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("邮箱地址不一致")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("这个邮箱已经被注册了")

        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")

        return super(UserRegisterForm, self).clean()