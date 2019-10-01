from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Article, Profile
from .utils import check_user


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles.html'


def show_article(request, id):
    article = get_object_or_404(Article, pk=id)
    user_id = check_user(request)
    current_user = get_object_or_404(Profile, pk=user_id)

    context = {
        'article': article,
        'current_user': current_user
    }

    return render(
        request,
        'article.html',
        context
    )

def subscribe(request):
    is_subscribe_toggle = bool(request.GET.get('subscribe_toggle', False))
    user_id = check_user(request)
    current_user = get_object_or_404(Profile, pk=user_id)

    if is_subscribe_toggle and current_user.is_paid_user:
        current_user.is_paid_user = False
    elif is_subscribe_toggle:
        current_user.is_paid_user = True
    current_user.save()

    context = {
        'current_user': current_user
    }

    return render(
        request,
        'subscription.html',
        context
    )
