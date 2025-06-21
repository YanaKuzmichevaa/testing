from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestNote(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_user = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug='slug',
            author=cls.author
        )

    def test_note_in_list_for_different_users(self):
        users_statuses = (
            (self.author, True),
            (self.other_user, False)
        )
        for user, note_in_list in users_statuses:
            self.client.force_login(user)
            with self.subTest(user=user):
                url = reverse('notes:list')
                response = self.client.get(url)
                objects_list = response.context['object_list']
                if note_in_list:
                    self.assertIn(self.note, objects_list)
                else:
                    self.assertNotIn(self.note, objects_list)

    def test_pages_contain_forms(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
