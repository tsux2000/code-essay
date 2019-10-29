from django.db import models
from django.utils import timezone
from sign.models import User
import uuid


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True,)
    is_official = models.BooleanField(default=False,)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    title = models.CharField(max_length=255,)
    contents = models.TextField()
    is_open = models.BooleanField(default=True,)
    create_date = models.DateField(default=timezone.now,)
    update_date = models.DateField(auto_now=True,)
    views = models.IntegerField(default=0,)
    likes = models.IntegerField(default=0,)
    del_flg = models.BooleanField(default=False,)


class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True,)
    name = models.CharField(max_length=255,)
    create_date = models.DateField(default=timezone.now,)
    update_date = models.DateField(auto_now=True,)
    del_flg = models.BooleanField(default=False,)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    contents = models.TextField()
    create_date = models.DateField(default=timezone.now,)
    update_date = models.DateField(auto_now=True,)
    goods = models.IntegerField(default=0,)
    bads = models.IntegerField(default=0,)
    del_flg = models.BooleanField(default=False,)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    articles = models.ManyToManyField('Article', blank=True,)

