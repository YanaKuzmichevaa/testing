from notes.forms import NoteForm
from .conftest import TestFixtures


class TestNote(TestFixtures):

    def test_note_in_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.other_user_client, False)
        )
        for user, note_in_list in users_statuses:
            with self.subTest(user=user):
                response = user.get(self.list_url)
                objects_list = response.context['object_list']
                self.assertIs((self.note in objects_list), note_in_list)

    def test_pages_contain_forms(self):
        for url in (self.add_url, self.edit_url):
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
