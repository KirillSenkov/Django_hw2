from django.shortcuts import render

from .models import Article, Tag, Scope

def articles_list(request):
    template = 'articles/news.html'

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = '-published_at'
    articles = Article.objects.all().prefetch_related(
        'scope__tag_id').order_by(
        ordering)
    for article in articles:
        article.sorted_scope = [(str(tag.tag_id), tag.is_main) for tag in
                                article.scope.all(
        ).order_by('-is_main', 'tag_id__name')]
    context = {'articles': articles}

    return render(request, template, context)


def tags_list(request):
    template = 'articles/tags.html'

    tags = Tag.objects.all().order_by(ordering)
    context = {'tags': tags}

    return render(request, template, context)