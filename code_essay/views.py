from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from code_essay.forms import ArticleForm
from code_essay.models import Article, Comment, Category
from sign.models import User
from django.urls import reverse_lazy
import math
import re
from django.http import HttpResponseBadRequest

DISP_NUM = 10

class IndexView(TemplateView):
    template_name = 'code_essay/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context


class CreateArticleView(CreateView):
    template_name = 'code_essay/article.html'
    form_class = ArticleForm
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_url = reverse_lazy('code_essay:article', article.pk)
        context.update({
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context


class ArticleView(TemplateView):

    template_name = 'code_essay/article.html'
    meta = {
        'robots': 'index, follow',
        'title': '',
    }

    def get(self, request, **kwargs):
        article_id = kwargs.get('article_id')
        article_slug = kwargs.get('article_slug')
        if article_id:
            try:
                self.article = Article.objects.get(pk=article_id)
            except Article.DoesNotExist:
                return HttpResponseBadRequest()
        elif article_slug:
            try:
                self.article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                return HttpResponseBadRequest()
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.article.views += 1
        self.article.save()
        self.meta['title'] = self.article.title
        context.update({
            'article': self.article,
            'category_list': Category.objects.filter(del_flg=False,),
            'comment_list': Comment.objects.filter(article=self.article),
            'meta': self.meta,
        })
        return context

    def post(self, request, **kwargs):
        # コメントの受け取り処理
        # 記事の修正受け取り処理
        # お気に入り受け取り処理n etc...
        pass


class ArticleListView(TemplateView):

    template_name = 'code_essay/article_list.html'
    meta = {
        'robots': 'noindex, follow',
        'title': 'ノート一覧',
    }
    user = {}
    articles = Article.objects.filter(del_flg=False, is_official=False, is_open=True,)

    def get(self, request, **kwargs):
        self.meta['title'] = 'ノート一覧'
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, page = kwargs.get('order_and_page')
        offset = (int(page) - 1) * DISP_NUM
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
            'article_list': self.articles.order_by(order)[offset:offset+DISP_NUM],
            'article_num': len(self.articles),
            'page': int(page),
            'page_nav': [i + 1 for i in range(math.ceil(len(self.articles) / DISP_NUM))],
            'page_nav_url': re.sub('page/[0-9]+/', '', self.request.path),
            'offset': offset + 1,
            'max_disp_num': min(offset + DISP_NUM, len(self.articles)),
            'display_user': self.user,
        })
        return context


class UserArticleListView(ArticleListView):

    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            self.user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        self.meta['title'] = '{} のノート一覧'.format(self.user.display_name)
        self.articles = Article.objects.filter(
            author=self.user,
            del_flg=False,
            is_official=False,
            is_open=True,
        )
        return super().get(request, **kwargs)


class CategoryArticleListView(ArticleListView):

    def get(self, request, **kwargs):
        category_slug = kwargs.get('category_slug')
        try:
            self.category = Category.objects.get(del_flg=False, slug=category_slug)
        except Category.DoesNotExist:
            return HttpResponseBadRequest()
        self.meta['title'] = '{} のノート一覧'.format(self.category.name)
        self.articles = Article.objects.filter(
            category=self.category,
            del_flg=False,
            is_official=False,
            is_open=True,
        )
        return super().get(request, **kwargs)


class OfficialArticleListView(ArticleListView):

    def get(self, request, **kwargs):
        self.articles = Article.objects.filter(del_flg=False, is_official=True, is_open=True,)
        self.meta['title'] = 'Code Essay 運営チーム'
        return super().get(request, **kwargs)

