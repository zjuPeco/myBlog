from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Successfully created</a>", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    if form.errors:
        messages.error(request, "Not successfully created")
    context = {
        "title": "创建表单",
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, detail_id=None):
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


def post_update(request, detail_id=None):
    instance = get_object_or_404(Post, id=detail_id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, detail_id=None):
    instance = get_object_or_404(Post, id=detail_id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:post_list")