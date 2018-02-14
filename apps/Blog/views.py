from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponse

# Create your views here.
class indexPage(View):
    def get(self, request):
        return render(request, "index.html")