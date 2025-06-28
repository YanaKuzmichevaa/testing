from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


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
