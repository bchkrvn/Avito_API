from django.urls import path, include
from rest_framework import routers

from authentication.views import user_views

router = routers.SimpleRouter()
router.register('', user_views.UsersGenericViewSet)

urlpatterns = [
    path('users/', include('authentication.all_urls.user_urls')),
    path('locations/', include('authentication.all_urls.location_urls')),
]

urlpatterns += router.urls
