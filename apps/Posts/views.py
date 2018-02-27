from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Post
from .forms import PostForm
from Comments.form import CommentForm
from Comments.models import Comment


# Create your views here.
def post_create(request):
    if not request.user.is_staff:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    if instance.draft:
        if request.user !=  instance.user and not request.user.is_staff and not request.user.is_superuser:
            raise Http404

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid() and request.user.is_authenticated:
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        parent_obj = None
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content=content_data,
            parent = parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "comment_form": comment_form
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.active().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
        )

    page_request_var = 'page'
    try:
        page = request.GET.get(page_request_var, 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(queryset_list, 3, request=request)
    queryset = p.page(page)

    context = {
        "title": "Peco的首页",
        "object_list": queryset,
        "page_request_var": page_request_var
    }
    return render(request, "index.html", context)


def post_update(request, id=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        response = HttpResponse("没有权限进行该操作")
        response.status_code = 403
        return response

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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


@login_required(login_url='accounts:login')
def post_delete(request, id=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Post, id=id)
    if instance.user != request.user:
        response = HttpResponse("没有权限进行该操作")
        response.status_code = 403
        return response

    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("posts:post_list")

    context = {
        'object': instance
    }
    return render(request, "confirm_delete.html", context)