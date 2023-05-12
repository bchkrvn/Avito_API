from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.response import Response

from ads.models import User
from ads.serializers.user_serializer import UserSerializers


class UsersGenericViewSet(viewsets.GenericViewSet):
    queryset = User.objects.prefetch_related('locations').annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username').all()
    serializer_class = UserSerializers

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk):
        user = self.get_object()
        data = request.data
        serializer = self.get_serializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response({'status': 'ok'}, status=204)
