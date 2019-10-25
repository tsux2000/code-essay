"""
URLルーティングを行うファイル. 各アプリケーションのurl.pyに接続する.
"""

from django.contrib import admin
from django.urls import path, include

# TODO: Media
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sign.urls')), # sign関連
    path('', include('code_essay.urls')), # メイン
]

# TODO: Media
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
