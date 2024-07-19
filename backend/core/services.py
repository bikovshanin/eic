from datetime import date, timedelta

from django.db import transaction

from house.models import Apartment, Tariff, WaterMeter, WaterMeterReading
from rent.models import CalculationResult


def calculate_water_cost(apartment, month):
    water_tariff = Tariff.objects.filter(is_water_tariff=True).first()

    if not water_tariff:
        raise ValueError("Water tariff not found")

    start_date = date(month.year, month.month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1)

    water_meters = WaterMeter.objects.filter(apartment=apartment)

    total_water_consumed = 0

    for meter in water_meters:

        current_reading = WaterMeterReading.objects.filter(
            water_meter=meter,
            reading_date__gte=start_date,
            reading_date__lt=end_date
        ).order_by('reading_date').first()

        previous_reading = WaterMeterReading.objects.filter(
            water_meter=meter,
            reading_date__lt=start_date
        ).order_by('-reading_date').first()

        if current_reading and previous_reading:
            total_water_consumed += (
                    current_reading.value - previous_reading.value
            )

    if total_water_consumed < 0:
        total_water_consumed = 0

    water_cost = total_water_consumed * water_tariff.price_per_unit

    return water_cost


def calculate_maintenance_cost(apartment):
    area_tariff = Tariff.objects.filter(is_area_tariff=True).first()
    maintenance_cost = apartment.area * float(area_tariff.price_per_unit)
    return maintenance_cost


def calculate_monthly_bill(apartment_id, month):
    apartment = Apartment.objects.get(pk=apartment_id)
    water_cost = calculate_water_cost(apartment, month)
    maintenance_cost = calculate_maintenance_cost(apartment)

    with transaction.atomic():
        result = CalculationResult.objects.create(
            apartment=apartment,
            month=month,
            water_cost=water_cost,
            maintenance_cost=maintenance_cost
        )

    return result
