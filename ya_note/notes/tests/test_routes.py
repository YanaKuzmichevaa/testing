from http import HTTPStatus

from .conftest import TestFixtures


class TestRoutes(TestFixtures):

    def test_pages_availability(self):
        parameters = (
            (self.home_url, self.client, 'get', HTTPStatus.OK),
            (self.login_url, self.client, 'get', HTTPStatus.OK),
            (self.logout_url, self.client, 'post', HTTPStatus.OK),
            (self.signup_url, self.client, 'get', HTTPStatus.OK),
            (self.add_url, self.author_client, 'get', HTTPStatus.OK),
            (self.list_url, self.author_client, 'get', HTTPStatus.OK),
            (self.success_url, self.author_client, 'get', HTTPStatus.OK),
            (self.edit_url, self.author_client, 'get', HTTPStatus.OK),
            (
                self.edit_url, self.other_user_client,
                'get', HTTPStatus.NOT_FOUND
            ),
            (self.delete_url, self.author_client, 'get', HTTPStatus.OK),
            (
                self.delete_url, self.other_user_client,
                'get', HTTPStatus.NOT_FOUND
            ),

        )
        for url, param_client, method, expected_status in parameters:
            with self.subTest(name=url):
                response = getattr(param_client, method)(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.add_url,
            self.list_url,
            self.success_url,
            self.detail_url,
            self.edit_url,
            self.delete_url
        )
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
