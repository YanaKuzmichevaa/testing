import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from http import HTTPStatus

from django.urls import reverse

from news.forms import WARNING
from news.models import Comment


def test_auth_user_can_post_comment(author_client, author, form_data, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_post_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, form_data, news, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = author_client.post(url, form_data)
    redirect_url = reverse('news:detail', args=(news.pk,))
    assertRedirects(response, f'{redirect_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_author_can_delete_comment(author_client, news, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = author_client.post(url)
    redirect_url = reverse('news:detail', args=(news.pk,))
    assertRedirects(response, f'{redirect_url}#comments')
    assert Comment.objects.count() == 0


def test_reader_cant_edit_other_comment(reader_client, comment, form_data):
    url = reverse('news:edit', args=(comment.pk,))
    response = reader_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_reader_cant_delete_other_comment(reader_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = reader_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_cant_use_bad_words(author_client, bad_words_data, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response.context['form'],
        'text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0
