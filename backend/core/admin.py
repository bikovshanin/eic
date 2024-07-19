from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


class BaseAdminModel(admin.ModelAdmin):
    """
    Базовая модель Админ панели.
    """

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
