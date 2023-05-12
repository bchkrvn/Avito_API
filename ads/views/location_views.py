from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serializers.location_serializer import LocationSerializers


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializers
