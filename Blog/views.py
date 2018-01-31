from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponse

# Create your views here.
class indexPage(View):
    def get(self, request):
        return HttpResponse("Hello world")