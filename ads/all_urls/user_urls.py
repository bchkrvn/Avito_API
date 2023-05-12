from django.urls import path, include
from rest_framework import routers

from ads.views import user_views

router = routers.SimpleRouter()
router.register('', user_views.UsersGenericViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
