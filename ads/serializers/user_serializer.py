from rest_framework import serializers

from ads.models import User, Location
from ads.serializers.location_serializer import LocationSerializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, max_length=20, required=True)
    role = serializers.CharField(write_only=True, max_length=10, required=True)
    locations = LocationSerializers(many=True, required=False)
    total_ads = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations') if 'locations' in self.initial_data else None
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if self._locations is not None:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)

        user.save()
        return user

    def save(self):
        user = super().save()

        if self._locations is not None:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)

        user.save()
        return user
