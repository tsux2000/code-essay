from code_essay.forms import ArticleForm
from code_essay.models import Article, Comment, Category
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from math import ceil
from re import sub
from sign.models import User


class IndexView(ListView):

    template_name = 'code_essay/index.html'
    model = Category
    paginate_by = 10
    queryset = Article.objects.filter(del_flg=False,)
    meta = {
        'robots': 'index, follow',
        'title': 'Topics',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context


class CreateArticleView(CreateView):
    template_name = 'code_essay/article.html'
    form_class = ArticleForm
    model = Article

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, '新しいノートを作成しました')
        self.success_url = reverse_lazy('code_essay:article', form.instance.pk)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class ArticleListView(ListView):

    template_name = 'code_essay/article_list.html'
    model = Article
    paginate_by = 10
    queryset = Article.objects.filter(del_flg=False, is_official=False, is_open=True,)
    meta = {
        'robots': 'noindex, follow',
        'title': 'ノート一覧',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context


class UserArticleListView(ListView):

    template_name = 'code_essay/article_list.html'
    model = Article
    paginate_by = 10
    queryset = Article.objects.filter(del_flg=False, is_official=False, is_open=True,)
    meta = {'robots': 'noindex, follow',}

    def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            self.user = User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.meta['title'] = '{} のノート一覧'.format(self.user.display_name)
        self.queryset = self.queryset.filter(author=self.user,)
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
            'display_user': self.user,
        })
        return context


class CategoryArticleListView(ListView):

    template_name = 'code_essay/article_list.html'
    model = Article
    paginate_by = 10
    queryset = Article.objects.filter(del_flg=False, is_official=False, is_open=True,)
    meta = {'robots': 'noindex, follow',}

    def get(self, request, **kwargs):
        category_slug = kwargs.get('category_slug')
        try:
            self.category = Category.objects.get(del_flg=False, slug=category_slug)
        except Category.DoesNotExist:
            return HttpResponseBadRequest()
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.meta['title'] = '{} のノート一覧'.format(self.category.name)
        self.queryset = self.queryset.filter(category=self.category,)
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context


class OfficialArticleListView(ListView):

    template_name = 'code_essay/article_list.html'
    model = Article
    paginate_by = 10
    queryset = Article.objects.filter(del_flg=False, is_official=True, is_open=True,)
    meta = {
        'robots': 'noindex, follow',
        'title': 'Code Essay 運営チーム',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'meta': self.meta,
            'category_list': Category.objects.filter(del_flg=False,),
        })
        return context
