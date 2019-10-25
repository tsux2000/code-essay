from django.urls import path
from sign.views import *

app_name = 'sign'

urlpatterns = [

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('sign_up/', SignUp.as_view(), name='sign_up'),
    path('sign_up/done', SignUpDone.as_view(), name='sign_up_done'),
    path('sign_up/complete/<token>/', SignUpComplete.as_view(), name='sign_up_complete'),

    path('user_update/<int:pk>/', UserUpdate.as_view(), name='user_update'),

    path('email_change/', EmailChange.as_view(), name='email_change'),
    path('email_change/done/', EmailChangeDone.as_view(), name='email_change_done'),
    path('email_change/complete/<str:token>/', EmailChangeComplete.as_view(), name='email_change_complete'),

    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),

    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),

]
