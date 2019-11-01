import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sign.models import User


class Article(models.Model):

    """
    Article（記事）モデル.
    """

    id = models.UUIDField(_('article uuid key'), primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(_('article slug'), max_length=255, unique=True, blank=True,)
    is_official = models.BooleanField(_('flag for official articles'), default=False,)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    title = models.CharField(_('article title'), max_length=255,)
    contents = models.TextField(_('article contents'), blank=True,)
    is_open = models.BooleanField(_('flag for published articles'), default=True,)
    create_date = models.DateField(_('create date'), default=timezone.now,)
    update_date = models.DateField(_('update date'), auto_now=True,)
    views = models.IntegerField(_('number of views'), default=0,)
    likes = models.IntegerField(_('number of likes'), default=0,)
    del_flg = models.BooleanField(_('flag for deleted articles'), default=False,)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class Category(models.Model):

    """
    Category（カテゴリ）モデル.
    """

    slug = models.SlugField(_('category slug'), max_length=255, unique=True, blank=True,)
    name = models.CharField(_('category name'), max_length=255,)
    create_date = models.DateField(_('create date'), default=timezone.now,)
    update_date = models.DateField(_('update date'), auto_now=True,)
    del_flg = models.BooleanField(_('flag for deleted categories'), default=False,)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Comment(models.Model):

    """
    Comment（コメント）モデル.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    contents = models.TextField(_('comment contents'), )
    create_date = models.DateField(_('create date'), default=timezone.now,)
    update_date = models.DateField(_('update date'), auto_now=True,)
    goods = models.IntegerField(_('number of user who evaluate this comment good'), default=0,)
    bads = models.IntegerField(_('number of user who evaluate this comment bad'), default=0,)
    del_flg = models.BooleanField(_('flag for deleted comments'), default=False,)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Favorite(models.Model):

    """
    Favorite（お気に入り）モデル. お気に入りをしたユーザーと, そのお気に入りをした記事を記録する.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    articles = models.ManyToManyField('Article', blank=True,)

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')

