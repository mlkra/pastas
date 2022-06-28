from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from pastas import models


class PastaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at')
    exclude = ('public_id',)
    readonly_fields = ('created_at', 'created_by', 'modified_at', 'public')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Pasta, PastaAdmin)
