from django.contrib import admin

from core.admin import BaseAdminModel
from rent.models import CalculationResult


class CalculationResultInline(admin.TabularInline):
    model = CalculationResult
    extra = 0


@admin.register(CalculationResult)
class CalculationResultAdmin(BaseAdminModel):
    list_display = (
        'apartment',
        'month',
        'water_cost',
        'maintenance_cost',
    )
    search_fields = (
        'apartment__number',
        'apartment__house__city',
        'apartment__house__street',
        'apartment__house__house_number',
    )
    readonly_fields = ('month',)

    fieldsets = (
        (None, {
            'fields': ('apartment', 'month', 'water_cost', 'maintenance_cost'),
            'classes': ['extrapretty'],
        }),
    )
