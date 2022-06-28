from typing import Optional

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from pastas.constants import PASTA_DETAIL, PASTA_DETAIL_PUBLIC, ACCOUNTS_PROFILE


class User(AbstractUser):
    @staticmethod
    def get_absolute_url() -> str:
        return reverse(ACCOUNTS_PROFILE)


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    modified_at = models.DateTimeField()
    public_id = models.UUIDField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-modified_at']

    @property
    def public(self):
        return True if self.public_id else False

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.pk:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Pasta, self).save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self) -> str:
        return reverse(PASTA_DETAIL, kwargs={'pk': self.pk})

    def get_public_url(self) -> Optional[str]:
        if self.public_id:
            return reverse(PASTA_DETAIL_PUBLIC, kwargs={'uuid': self.public_id})
        return None
