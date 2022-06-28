import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UsernameField

from pastas import models

User = get_user_model()


class PastaForm(forms.ModelForm):
    public = forms.BooleanField(required=False)

    class Meta:
        model = models.Pasta
        fields = ['name', 'text', 'public']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['public'].initial = self.instance.public

    def save(self, commit=True) -> models.Pasta:
        if not self.instance.pk:
            self.instance.created_by = self.user
        pasta_visibility_changed = self._field_has_changed('public')
        if pasta_visibility_changed:
            if self.cleaned_data['public']:
                self.instance.public_id = uuid.uuid4()
            else:
                self.instance.public_id = None
        return super(PastaForm, self).save(commit)

    def _field_has_changed(self, field_name: str):
        return True if field_name in self.changed_data else False


class PastaPublicForm(forms.ModelForm):
    class Meta:
        model = models.Pasta
        fields = ['name', 'text']

    def save(self, commit=True) -> models.Pasta:
        if not self.instance.pk:
            self.instance.public_id = uuid.uuid4()
        return super(PastaPublicForm, self).save(commit)


class UserCreationForm(AuthUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
