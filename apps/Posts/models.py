from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from markdown_deux import markdown
from Comments.models import Comment


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)


def upload_location(instance, filename):
    return "{0}/{1}".format(int(instance.id), filename)


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="题目")
    abstract = models.CharField(max_length=300, null=True, blank=True, verbose_name="摘要")
    github_url = models.CharField(max_length=200, null=True, blank=True, verbose_name="github地址")
    # slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True,
                              width_field="width_field",
                              height_field="height_field",
                              verbose_name="封面图")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False, verbose_name="草稿")
    publish = models.DateField(auto_now=False, auto_now_add=False, verbose_name="发表日期")
    content = models.TextField(verbose_name="文章内容")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="生成时间")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("posts:post_update", kwargs={"id": self.id})

    def get_markdown(self):
        content = self.content
        # markdown_text = markdown(content)
        # return mark_safe(markdown_text)
        return content

    @property
    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type

    class Meta():
        # verbose_name = '博客文章'
        # verbose_name_plural = verbose_name
        ordering = ["-timestamp", "-updated"]


def create_slug(slug, count=1):
    new_slug = "%s-%s" % (slug, count)
    exists = Post.objects.filter(slug=new_slug).exists()
    if exists:
        return create_slug(slug, count + 1)
    return new_slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if not exists:
        instance.slug = slug
    else:
        instance.slug = create_slug(slug)


# url中有中文不太好
# pre_save.connect(pre_save_post_receiver, sender=Post)