import uuid
from typing import Optional

from django.contrib.auth import get_user_model
from django.test import TestCase

from pastas import forms, models

User = get_user_model()


class PastaFormTestCase(TestCase):
    def test_new_public_pasta_generates_public_id(self):
        form = self._create_and_validate_pasta_form(public=True)

        pasta = form.save()

        self.assertTrue(pasta.public)
        self.assertIsNotNone(pasta.public_id)

    def test_new_private_pasta_created_without_public_id(self):
        form = self._create_and_validate_pasta_form(public=False)

        pasta = form.save()

        self.assertFalse(pasta.public)
        self.assertIsNone(pasta.public_id)

    def test_making_pasta_private_deletes_public_id(self):
        pasta = _create_pasta(public_id=uuid.uuid4())
        form = self._create_and_validate_pasta_form(public=False, instance=pasta)

        pasta = form.save()

        self.assertFalse(pasta.public)
        self.assertIsNone(pasta.public_id)

    def test_making_pasta_public_creates_public_id(self):
        pasta = _create_pasta()
        form = self._create_and_validate_pasta_form(public=True, instance=pasta)

        pasta = form.save()

        self.assertTrue(pasta.public)
        self.assertIsNotNone(pasta.public_id)

    def test_user_that_created_pasta_is_saved(self):
        user = User.objects.create_user('Username')
        form = self._create_and_validate_pasta_form(user=user)

        pasta = form.save()

        self.assertEqual(pasta.created_by, user)

    @staticmethod
    def _create_and_validate_pasta_form(public=False, instance: Optional[models.Pasta] = None,
                                        user: Optional[User] = None) -> forms.PastaForm:
        form = forms.PastaForm({'name': 'Name', 'text': 'Text.', 'public': public}, instance=instance, user=user)
        form.is_valid()
        return form


class PastaPublicFormTestCase(TestCase):
    def test_creating_pasta_generates_public_id(self):
        form = self._create_and_validate_pasta_form()

        pasta = form.save()

        self.assertTrue(pasta.public)

    @staticmethod
    def _create_and_validate_pasta_form():
        form = forms.PastaPublicForm({'name': 'Name', 'text': 'Text.'})
        form.is_valid()
        return form


def _create_pasta(public_id=None) -> models.Pasta:
    pasta = models.Pasta.objects.create(name='Name', text='Text.', public_id=public_id)
    return pasta
