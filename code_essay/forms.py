from django import forms
from code_essay.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('contents',)

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
