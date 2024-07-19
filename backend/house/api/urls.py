from django.urls import include, path
from rest_framework.routers import DefaultRouter

from house.api.views import (ApartmentDetailView, ApartmentListView,
                             HouseViewSet)

router = DefaultRouter()
router.register(r'houses', HouseViewSet, basename='house')

house_urlpatterns = [
    path('', include(router.urls)),
    path(
        'apartments/',
        ApartmentListView.as_view(),
        name='apartment-list'
    ),
    path(
        'apartment_detail/',
        ApartmentDetailView.as_view(),
        name='apartment_detail'
    ),
]
