from django.urls import path

from rent.api.views import CalculationView

rent_urlpatterns = [
    path('calculate_bills/<int:house_id>/', CalculationView.as_view(),
         name='calculate_house_bills')
]
