from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from sign.forms import *


User = get_user_model()


class Login(LoginView):

    form_class = LoginForm
    template_name = 'sign/sign.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'Sign in',
        }
        context.update({
            'meta': meta,
            'submit_button_text': 'Sign in',
        })
        return context


class Logout(LoginRequiredMixin, LogoutView):

    template_name = 'sign/message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'Logout',
        }
        context.update({
            'meta': meta,
            'message': 'ログアウトしました。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class SignUp(CreateView):

    template_name = 'sign/sign.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'Sign up',
        }
        context.update({
            'meta': meta,
            'submit_button_text': 'Sign up',
        })
        return context

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.display_name = user.email.split('@')[0]
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('sign/mail_template/sign_up_subject.tpl', context).rstrip('\n')
        contents = render_to_string('sign/mail_template/sign_up_contents.tpl', context)
        user.email_user(subject, contents)

        return redirect('sign:sign_up_done')


class SignUpDone(TemplateView):

    template_name = 'sign/message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': '仮登録完了 - Sign up',
        }
        context.update({
            'meta': meta,
            'message': '本登録用メールを送信しました。メールに記載のリンクをクリックして本登録を完了してください。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class SignUpComplete(TemplateView):

    template_name = 'sign/message.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*30)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': '完了 - Sign up',
        }
        context.update({
            'meta': meta,
            'message': 'アカウントを作成しました。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context

    def get(self, request, **kwargs):

        token = kwargs.get('token')

        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserUpdate(OnlyYouMixin, UpdateView):

    model = User
    form_class = UserUpdateForm
    template_name = 'code_essay/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'ユーザー情報更新 - {}'.format(self.request.user.display_name),
        }
        context.update({
            'meta': meta,
        })
        return context

    def get_success_url(self):
        return resolve_url('sign:user_update', pk=self.kwargs['pk'])


class EmailChange(LoginRequiredMixin, FormView):

    template_name = 'code_essay/user.html'
    form_class = EmailChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'メールアドレス変更 - {}'.format(self.request.user.display_name),
        }
        context.update({
            'meta': meta,
        })
        return context

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('sign/mail_template/email_change_subject.tpl', context)
        message = render_to_string('sign/mail_template/email_change_message.tpl', context)
        send_mail(subject, message, None, [new_email])

        return redirect('sign:email_change_done')


class EmailChangeDone(LoginRequiredMixin, TemplateView):

    template_name = 'sign/message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'メール送信完了',
        }
        context.update({
            'meta': meta,
            'message': 'メールアドレス変更用メールを送信しました。メールに記載のリンクをクリックして変更を完了してください。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class EmailChangeComplete(LoginRequiredMixin, TemplateView):

    template_name = 'sign/message.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*30)

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'メールアドレス変更完了',
        }
        context.update({
            'meta': meta,
            'message': 'メールアドレスを変更しました。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('sign:password_change_done')
    template_name = 'code_essay/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'パスワード変更 - {}'.format(self.request.user.display_name),
        }
        context.update({
            'meta': meta,
        })
        return context


class PasswordChangeDone(PasswordChangeDoneView):

    template_name = 'sign/message.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'パスワード変更完了',
        }
        context.update({
            'meta': meta,
            'message': 'パスワードを更新しました。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class PasswordReset(PasswordResetView):

    subject_template_name = 'sign/mail_template/password_reset_subject.tpl'
    email_template_name = 'sign/mail_template/password_reset_message.tpl'
    template_name = 'code_essay/user.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('sign:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'パスワードのリセット',
        }
        context.update({
            'meta': meta,
        })
        return context


class PasswordResetDone(PasswordResetDoneView):

    template_name = 'sign/message.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'メール送信完了',
        }
        context.update({
            'meta': meta,
            'message': 'パスワードリセット用のメールを送信しました。メールに記載のリンクをクリックして変更を完了してください。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context


class PasswordResetConfirm(PasswordResetConfirmView):

    form_class = MySetPasswordForm
    success_url = reverse_lazy('sign:password_reset_complete')
    template_name = 'code_essay/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'パスワードのリセット'.format(self.request.user.display_name),
        }
        context.update({
            'meta': meta,
        })
        return context


class PasswordResetComplete(PasswordResetCompleteView):

    template_name = 'sign/message.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = {
            'title': 'パスワードリセット完了',
        }
        context.update({
            'meta': meta,
            'message': 'パスワードを変更しました。',
            'submit_button_text': 'トップページへ',
            'link_to': '/article/',
        })
        return context
