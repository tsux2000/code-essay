from code_essay.views import (
    ArticleListView,
    ArticleView,
    CategoryArticleListView,
    CreateArticleView,
    IndexView,
    OfficialArticleListView,
    UserArticleListView,
)
from code_essay.converters import OrderAndPageConverter
from django.urls import register_converter, path


app_name = 'code_essay'

urlpatterns = [
    path('', IndexView.as_view(), name='index'), # トップページ
    path('article_list/', ArticleListView.as_view(), name='article_list'), # 記事一覧ページ
    path('user/<uuid:user_id>/', UserArticleListView.as_view(), name='user'), # ユーザー記事一覧ページ
    path('category/<slug:category_slug>/', CategoryArticleListView.as_view(), name='category'), # カテゴリページ
    path('official/', OfficialArticleListView.as_view(), name='official'), # 公式記事一覧ページ
    path('new/', CreateArticleView.as_view(), name='new'), # 新規記事作成ページ
    path('article/<uuid:article_id>/', ArticleView.as_view(), name='article'), # 記事ページ
    path('<slug:article_slug>/', ArticleView.as_view(), name='article_slug'), # 記事ページ（slug）
]
