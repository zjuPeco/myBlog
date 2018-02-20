from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, detail_id):
    instance = get_object_or_404(Post, id=detail_id)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()

    context = {
        "title": "Peco的首页",
        "object_list": queryset
    }

    return render(request, "index.html", context)


def post_update(request):
    return HttpResponse("<h1>update</h1>")


def post_delete(request):
    return HttpResponse("<h1>delete</h1>")