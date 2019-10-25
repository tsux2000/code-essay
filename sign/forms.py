from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'username':
                placeholder = 'Email'
            elif key == 'password':
                placeholder = 'Password'
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'sign__form-item',
                'placeholder': placeholder,
            })


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'email':
                placeholder = 'Email - Required'
            elif key == 'password1':
                placeholder = 'Password - Required'
            elif key == 'password2':
                placeholder = 'Password - Confirm'
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'sign__form-item',
                'placeholder': placeholder,
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'display_name', 'bio',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'name':
                placeholder = 'Your full name'
            elif key == 'display_name':
                placeholder = 'Others can see your display name.'
                field.label = '表示名'
            elif key == 'bio':
                placeholder = 'Message'
                field.label = 'ひとこと'
                field.widget.attrs['rows'] = 5
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'user__form-item',
                'placeholder': placeholder,
            })


class EmailChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'user__form-item',
                'placeholder': 'New email address - Required',
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'old_password':
                placeholder = 'Old password - Required'
            elif key == 'new_password1':
                placeholder = 'New Password - Required'
            elif key == 'new_password2':
                placeholder = 'New Password - Confirm'
                field.label = '新しいパスワード（確認）'
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'user__form-item',
                'placeholder': placeholder,
            })


class MyPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'old_password':
                placeholder = 'Old password - Required'
            elif key == 'new_password1':
                placeholder = 'New Password - Required'
            elif key == 'new_password2':
                placeholder = 'New Password - Confirm'
                field.label = '新しいパスワード（確認）'
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'user__form-item',
                'placeholder': placeholder,
            })


class MySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'old_password':
                placeholder = 'Old password - Required'
            elif key == 'new_password1':
                placeholder = 'New Password - Required'
            elif key == 'new_password2':
                placeholder = 'New Password - Confirm'
                field.label = '新しいパスワード（確認）'
            else:
                placeholder = ''
            field.widget.attrs.update({
                'class': 'user__form-item',
                'placeholder': placeholder,
            })

