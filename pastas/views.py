from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from pastas import models, forms
from pastas.constants import PASTA_DETAIL, PASTA_ADD, PASTAS_LIST, PASTA_UPDATE, PASTA_PUBLIC_ADD
from pastas.forms import UserCreationForm

User = get_user_model()


class PastaHomePageView(generic.TemplateView):
    template_name = 'pastas/pasta_home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse(PASTAS_LIST))
        else:
            return super(PastaHomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super(PastaHomePageView, self).get_context_data(**kwargs)
        context['PASTA_PUBLIC_ADD'] = PASTA_PUBLIC_ADD
        return context


class PastasListView(LoginRequiredMixin, generic.ListView):
    model = models.Pasta

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        context = super(PastasListView, self).get_context_data(**kwargs)
        context['PASTA_ADD'] = PASTA_ADD
        context['PASTA_DETAIL'] = PASTA_DETAIL
        return context


class PastaDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Pasta

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PastaDetailView, self).get_context_data(**kwargs)
        context['PASTA_UPDATE'] = PASTA_UPDATE
        return context


class PastaCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Pasta
    form_class = forms.PastaForm

    def get_form_kwargs(self):
        kwargs = super(PastaCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PastaPublicCreateView(generic.CreateView):
    template_name = 'pastas/pasta_public_form.html'
    model = models.Pasta
    form_class = forms.PastaPublicForm

    def get_success_url(self):
        return self.object.get_public_url()


class PastaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Pasta
    form_class = forms.PastaForm

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PastaUpdateView, self).get_context_data(**kwargs)
        context['PASTA_DETAIL'] = PASTA_DETAIL
        return context


class PastaPublicDetailView(generic.DetailView):
    model = models.Pasta
    template_name = 'pastas/pasta_detail_public.html'
    slug_field = 'public_id'
    slug_url_kwarg = 'uuid'


class AccountProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/profile.html'


class AccountCreateView(generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/user_form.html'
