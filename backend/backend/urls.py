from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from house.api.urls import house_urlpatterns
from rent.api.urls import rent_urlpatterns

v1_urls = [
    path('', include((house_urlpatterns, 'house'))),
    path('', include((rent_urlpatterns, 'rent')))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1_urls)),
    path(
        'redoc/',
        TemplateView.as_view(
            template_name='redoc.html',
        ), name='redoc'
    ),
]
