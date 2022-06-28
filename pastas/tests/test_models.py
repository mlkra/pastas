from datetime import datetime, timezone

from django.test import TestCase
from freezegun import freeze_time

from pastas import models


class PastaTestCase(TestCase):
    def test_saving_new_pasta_saves_creation_and_modification_date(self):
        date_now = datetime(2022, 7, 7, 7, 0, 0, tzinfo=timezone.utc)

        with freeze_time(date_now):
            pasta = _create_pasta()

        self.assertEqual(pasta.created_at, date_now)
        self.assertEqual(pasta.modified_at, date_now)

    def test_saving_existing_pasta_saves_modification_date(self):
        with freeze_time(datetime(2022, 7, 7, 7, 0, 0, tzinfo=timezone.utc)):
            pasta = _create_pasta()
        date_now = datetime(2022, 7, 7, 7, 0, 0, tzinfo=timezone.utc)
        pasta.name = 'New name'

        with freeze_time(date_now):
            pasta.save()

        self.assertEqual(pasta.modified_at, date_now)


def _create_pasta() -> models.Pasta:
    pasta = models.Pasta.objects.create(name='Name', text='Text.')
    return pasta
