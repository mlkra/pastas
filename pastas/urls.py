"""pastas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pastas import constants
from pastas import views

PASTAS_PATH = 'pastas'

urlpatterns = [
    path('', views.PastaHomePageView.as_view(), name=constants.PASTA_HOME),
    path(f'{PASTAS_PATH}/', views.PastasListView.as_view(), name=constants.PASTAS_LIST),
    path(f'{PASTAS_PATH}/<int:pk>', views.PastaDetailView.as_view(), name=constants.PASTA_DETAIL),
    path(f'{PASTAS_PATH}/<int:pk>/update', views.PastaUpdateView.as_view(), name=constants.PASTA_UPDATE),
    path(f'{PASTAS_PATH}/add', views.PastaCreateView.as_view(), name=constants.PASTA_ADD),
    path(f'{PASTAS_PATH}/public/<uuid:uuid>', views.PastaPublicDetailView.as_view(),
         name=constants.PASTA_DETAIL_PUBLIC),
    path(f'{PASTAS_PATH}/public/add', views.PastaPublicCreateView.as_view(), name=constants.PASTA_PUBLIC_ADD),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create/', views.AccountCreateView.as_view(), name=constants.ACCOUNT_CREATE),
    path('accounts/profile/', views.AccountProfileView.as_view(), name=constants.ACCOUNTS_PROFILE),
    path('admin/', admin.site.urls),
]
