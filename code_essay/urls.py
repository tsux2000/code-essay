from django.urls import path
from code_essay.views import *

app_name = 'code_essay'

urlpatterns = [
    # path('index/', IndexView.as_view(), name='index'),
    path('article/', ArticleView.as_view(), name='article'),
    path('user/<int:pk>/', ArticleView.as_view(), name='user'),
    # path('list/', ListView.as_view(), name='list'),
    # path('sign/', SignView.as_view(), name='sign'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]
