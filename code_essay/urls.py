from django.urls import register_converter, path
from code_essay.views import *
import re

class OrderAndPageConverter:

    regex = '((order/[a-z0-9_\-]+/)|(page/[0-9]+/)){0,2}'

    def to_python(self, value):
        order = re.search(r'order/([a-z0-9_\-]+)/', value)
        self.order = str(order[1]) if order else '-create_date'
        page = re.search(r'page/([0-9]+)/', value)
        self.page = str(page[1]) if page else '1'
        self.page = self.page if int(self.page) else '1'
        return self.order, self.page

    def to_url(self, value):
        return str(value)

register_converter(OrderAndPageConverter, 'order_and_page')

app_name = 'code_essay'

urlpatterns = [

    path('', IndexView.as_view(), name='index'),

    path('article_list/<order_and_page:order_and_page>', ArticleListView.as_view(), name='article_list'),

    path('user/<uuid:user_id>/<order_and_page:order_and_page>', UserArticleListView.as_view(), name='user'),

    path('category/<slug:category_slug>/<order_and_page:order_and_page>', CategoryArticleListView.as_view(), name='category'),

    path('official/<order_and_page:order_and_page>', OfficialArticleListView.as_view(), name='official'),

    path('new/', CreateArticleView.as_view(), name='new'),

    path('article/<uuid:article_id>/', ArticleView.as_view(), name='article'),
    path('<slug:article_slug>/', ArticleView.as_view(), name='article_slug'),

]
