from django.shortcuts import render
from django.views.generic import TemplateView


class ArticleView(TemplateView):
    template_name = 'code_essay/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Code Essay',
        })
        return context
