import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture
from django.urls import reverse

from http import HTTPStatus


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


HOME_URL = lazy_fixture('home_url')
DETAIL_URL = lazy_fixture('detail_url')
LOGIN_URL = lazy_fixture('login_url')
LOGOUT_URL = lazy_fixture('logout_url')
SIGNUP_URL = lazy_fixture('signup_url')
EDIT_URL = lazy_fixture('edit_url')
DELETE_URL = lazy_fixture('delete_url')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, parametrized_client, method, expected_status',
    [
        (HOME_URL, lazy_fixture('client'), 'get', HTTPStatus.OK),
        (DETAIL_URL, lazy_fixture('client'), 'get', HTTPStatus.OK),
        (LOGIN_URL, lazy_fixture('client'), 'get', HTTPStatus.OK),
        (SIGNUP_URL, lazy_fixture('client'), 'get', HTTPStatus.OK),
        (LOGOUT_URL, lazy_fixture('client'), 'post', HTTPStatus.OK),
        (EDIT_URL, lazy_fixture('author_client'), 'get', HTTPStatus.OK),
        (EDIT_URL, lazy_fixture('reader_client'), 'get', HTTPStatus.NOT_FOUND),
        (DELETE_URL, lazy_fixture('author_client'), 'get', HTTPStatus.OK),
        (
            DELETE_URL,
            lazy_fixture('reader_client'),
            'get',
            HTTPStatus.NOT_FOUND
        )
    ]
)
def test_pages_availability(
    name, parametrized_client, method, expected_status
):
    url = name
    response = getattr(parametrized_client, method)(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (EDIT_URL, DELETE_URL)
)
def test_redirects(client, name, login_url):
    url = name
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
