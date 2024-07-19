from django.contrib import admin

from core.admin import BaseAdminModel
from house.models import (Apartment, House, Tariff, WaterMeter,
                          WaterMeterReading)
from rent.admin import CalculationResultInline


class ApartmentInline(admin.TabularInline):
    model = Apartment
    extra = 0


class WaterMeterInline(admin.TabularInline):
    model = WaterMeter
    extra = 0


class WaterMeterReadingInline(admin.TabularInline):
    model = WaterMeterReading
    extra = 0


@admin.register(House)
class HouseAdmin(BaseAdminModel):
    list_display = ('city', 'street', 'house_number')
    search_fields = ('city', 'street', 'house_number')
    inlines = [ApartmentInline]

    fieldsets = (
        (
            None, {
                'fields': ('city', 'street', 'house_number'),
                'classes': ['extrapretty'],
            }
        ),
    )


@admin.register(Apartment)
class ApartmentAdmin(BaseAdminModel):
    list_display = ('number', 'house', 'area')
    search_fields = (
        'number',
        'house__city',
        'house__street',
        'house__house_number'
    )
    inlines = [WaterMeterInline, CalculationResultInline]

    fieldsets = (
        (
            None, {
                'fields': ('number', 'house', 'area'),
                'classes': ['extrapretty'],
            }
        ),
    )


@admin.register(WaterMeter)
class WaterMeterAdmin(BaseAdminModel):
    list_display = ('name', 'serial_number', 'apartment')
    search_fields = (
        'name',
        'serial_number',
        'apartment__number',
        'apartment__house__city',
        'apartment__house__street',
        'apartment__house__house_number',
    )
    inlines = [WaterMeterReadingInline]

    fieldsets = (
        (
            None, {
                'fields': ('name', 'serial_number', 'apartment'),
                'classes': ['extrapretty'],
            }
        ),
    )


@admin.register(WaterMeterReading)
class WaterMeterReadingAdmin(BaseAdminModel):
    list_display = ('water_meter', 'reading_date', 'value')
    search_fields = (
        'water_meter__name',
        'water_meter__serial_number',
        'water_meter__apartment__number',
        'water_meter__apartment__house__city',
        'water_meter__apartment__house__street',
        'water_meter__apartment__house__house_number',
    )
    readonly_fields = ('reading_date',)

    fieldsets = (
        (
            None, {
                'fields': ('water_meter', 'reading_date', 'value'),
                'classes': ['extrapretty'],
            }
        ),
    )


@admin.register(Tariff)
class TariffAdmin(BaseAdminModel):
    list_display = (
        'name',
        'price_per_unit',
        'is_water_tariff',
        'is_area_tariff'
    )
    search_fields = ('name',)

    fieldsets = (
        (
            None, {
                'fields': (
                    'name', 'price_per_unit', 'is_water_tariff',
                    'is_area_tariff'),
                'classes': ['extrapretty'],
            }
        ),
    )
