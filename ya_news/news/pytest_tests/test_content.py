from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_count_news(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(client, comments, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timesteps = [comment.created for comment in all_comments]
    sorted_timestaps = sorted(all_timesteps)
    assert all_timesteps == sorted_timestaps


def test_form_for_auth_user(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_no_form_for_anonymous(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'form' not in response.context
