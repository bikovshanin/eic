from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core.services import calculate_monthly_bill
from house.models import Apartment, WaterMeterReading


@shared_task
def calculate_bills_for_house(house_id, month):
    apartments = Apartment.objects.filter(house_id=house_id)
    results = []
    for apartment in apartments:
        result = calculate_monthly_bill(apartment.id, month)
        results.append(result.id)
    return results


@shared_task
def delete_old_readings():
    three_months_ago = timezone.now() - timedelta(days=90)
    old_readings = WaterMeterReading.objects.filter(
        reading_date__lt=three_months_ago
    )
    old_readings.delete()
