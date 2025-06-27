from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestFixtures(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_user = User.objects.create(username='Не автор')
        cls.other_user_client = Client()
        cls.other_user_client.force_login(cls.other_user)
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='slug',
            author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.slug_for_args = cls.note.slug
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.edit_url = reverse('notes:edit', args=(cls.slug_for_args,))
        cls.detail_url = reverse('notes:detail', args=(cls.slug_for_args,))
        cls.delete_url = reverse('notes:delete', args=(cls.slug_for_args,))
        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
