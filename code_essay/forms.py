from django import forms
from code_essay.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('contents', 'category', 'title', 'is_open')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key == 'contents':
                class_name = ''
                id_name = 'js-article__textarea'
            elif key == 'category':
                class_name = ''
                id_name = ''
            elif key == 'title':
                class_name = ''
                id_name = ''
            elif key == 'is_open':
                class_name = ''
                id_name = ''
            field.widget.attrs.update({
                'class': class_name,
                'id': id_name,
            })
