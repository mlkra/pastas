import re
from typing import Protocol

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from pastas.constants import PASTAS_LIST, PASTA_DETAIL, PASTA_ADD, PASTA_UPDATE, PASTA_HOME, PASTA_PUBLIC_ADD, \
    ACCOUNT_CREATE, ACCOUNTS_PROFILE, ACCOUNTS_LOGIN

User = get_user_model()
USER_PASSWORD = 'Qwertyuiop1!'


class PastaHomePageViewTestCase(TestCase):
    def test_unauthorized_user_sees_sign_in_link(self):
        response = self._get_pasta_home()

        self.assertContains(response, 'Sign in')

    def test_authorized_user_is_redirected_to_pastas_list(self):
        _create_and_login_user(self.client)

        response = self._get_pasta_home()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(PASTAS_LIST))

    def _get_pasta_home(self) -> HttpResponseRedirect:
        return self.client.get(reverse(PASTA_HOME))


class HasClient(Protocol):
    client: Client


class LoginRequiredViewTestCaseMixin:
    def setUp(self: HasClient):
        _create_and_login_user(self.client)


class PastaListViewTestCase(LoginRequiredViewTestCaseMixin, TestCase):
    def test_no_pastas(self):
        response = self._get_pastas_list()

        self.assertContains(response, 'No pastas are available.')

    def test_all_pastas_shown(self):
        pasta1 = 'First pasta.'
        pasta2 = 'Second pasta.'
        _add_pasta(self.client, name=pasta1)
        _add_pasta(self.client, name=pasta2)

        response = self._get_pastas_list()

        self.assertContains(response, pasta1)
        self.assertContains(response, pasta2)

    def test_pasta_created_by_different_user_is_not_shown(self):
        _, pk = _add_pasta(self.client, name='Name')
        _create_and_login_user(self.client, 'username2')

        response = self._get_pastas_list()

        self.assertContains(response, 'No pastas are available.')

    def _get_pastas_list(self) -> HttpResponseRedirect:
        return self.client.get(reverse(PASTAS_LIST))


class PastaDetailViewTestCase(LoginRequiredViewTestCaseMixin, TestCase):
    def test_existing_pasta(self):
        pasta_name = 'Name'
        pasta_text = 'Text.'
        _, pk = _add_pasta(self.client, name=pasta_name, text=pasta_text)

        response = self._get_pasta_detail(pk)

        self.assertContains(response, pasta_name)
        self.assertContains(response, pasta_text)

    def test_pasta_created_by_different_user_is_inaccessible(self):
        _, pk = _add_pasta(self.client, name='Name')
        _create_and_login_user(self.client, 'username2')

        response = self._get_pasta_detail(pk)

        self.assertEqual(response.status_code, 404)

    def _get_pasta_detail(self, pk: int) -> HttpResponseRedirect:
        return self.client.get(reverse(PASTA_DETAIL, kwargs={'pk': pk}))


class PastaCreateViewTestCase(LoginRequiredViewTestCaseMixin, TestCase):
    def test_adding_pasta(self):
        new_pasta_name = 'Name'
        new_pasta_text = 'Text.'

        response, _ = _add_pasta(self.client, name=new_pasta_name, text=new_pasta_text)

        response = self.client.get(response.url)
        self.assertContains(response, new_pasta_name)
        self.assertContains(response, new_pasta_text)


class PastaPublicCreateViewTestCase(TestCase):
    def test_adding_public_pasta(self):
        new_pasta_name = 'Name'
        new_pasta_text = 'Text.'

        response, _ = self._add_public_pasta(name=new_pasta_name, text=new_pasta_text)

        response = self.client.get(response.url)
        self.assertContains(response, new_pasta_name)
        self.assertContains(response, new_pasta_text)

    def _add_public_pasta(self, name: str, text='Text.') -> tuple[HttpResponseRedirect, int]:
        response = self.client.post(reverse(PASTA_PUBLIC_ADD), {'name': name, 'text': text})
        pk = re.search(r'\d', response.url)[0]
        return response, pk


class PastaUpdateViewTestCase(LoginRequiredViewTestCaseMixin, TestCase):
    def test_updating_pasta(self):
        pasta_name = 'Name'
        pasta_text = 'Text.'
        new_pasta_name = 'Eman'
        new_pasta_text = 'Txet.'
        _, pk = _add_pasta(self.client, name=pasta_name, text=pasta_text)

        response = self._update_pasta(pk, new_name=new_pasta_name, new_text=new_pasta_text)

        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertNotContains(response, pasta_name)
        self.assertNotContains(response, pasta_text)
        self.assertContains(response, new_pasta_name)
        self.assertContains(response, new_pasta_text)

    def test_pasta_created_by_different_user_is_inaccessible(self):
        _, pk = _add_pasta(self.client, name='Name')
        _create_and_login_user(self.client, 'username2')
        new_pasta_name = 'Eman'

        response = self._update_pasta(pk, new_name=new_pasta_name)

        self.assertEqual(response.status_code, 404)

    def _update_pasta(self, pk: int, new_name='Name', new_text='Text.') -> HttpResponseRedirect:
        return self.client.post(reverse(PASTA_UPDATE, kwargs={'pk': pk}), {'name': new_name, 'text': new_text})


class AccountCreateViewTestCase(TestCase):
    def test_create_user(self):
        response = _create_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(ACCOUNTS_PROFILE))


def _add_pasta(client: Client, name: str, text='Text.') -> tuple[HttpResponseRedirect, int]:
    response = client.post(reverse(PASTA_ADD), {'name': name, 'text': text})
    pk = re.search(r'\d', response.url)[0]
    return response, pk


def _create_user(client: Client, username='username') -> HttpResponseRedirect:
    response = client.post(reverse(ACCOUNT_CREATE),
                           {'username': username, 'password1': USER_PASSWORD, 'password2': USER_PASSWORD})
    return response


def _login_user(client: Client, username='username'):
    client.post(reverse(ACCOUNTS_LOGIN), {'username': username, 'password': USER_PASSWORD})


def _create_and_login_user(client: Client, username='username'):
    _create_user(client, username)
    _login_user(client, username)
