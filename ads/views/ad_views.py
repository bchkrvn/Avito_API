from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework import viewsets
from rest_framework.response import Response

from ads.models import Ad
from ads.serializers.ad_serializer import AdSerializer


@method_decorator(csrf_exempt, name="dispatch")
class AdImageUploadView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        img = request.FILES['image']
        extension = img.name.rsplit('.', 1)[1].lower()
        img.name = f'post{ad.id}.{extension}'
        ad.image = img
        ad.save()

        return JsonResponse({'id': ad.id, 'image': ad.image.url})


class AdGenericViewSet(viewsets.GenericViewSet):
    queryset = Ad.published.select_related('author').select_related('category').all()
    serializer_class = AdSerializer

    def list(self, request):
        category = request.GET.get('cat')
        text = request.GET.get('text')
        location = request.GET.get('location')
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')

        if category:
            self.queryset = self.get_queryset().filter(category=category)
        if text:
            self.queryset = self.get_queryset().filter(name__icontains=text)
        if location:
            self.queryset = self.get_queryset().filter(author__locations__name__icontains=location)
        if price_from:
            self.queryset = self.get_queryset().filter(price__gte=price_from)
        if price_to:
            self.queryset = self.get_queryset().filter(price__lte=price_to)

        queryset = self.get_queryset().order_by('-price')
        serializer = self.get_serializer(queryset, many=True)
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
        ad = self.get_object()
        data = request.data
        serializer = self.get_serializer(ad, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk):
        ad = self.get_object()
        data = request.data
        serializer = self.get_serializer(ad, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, pk):
        ad = self.get_object()
        ad.delete()
        return Response({'status': 'ok'}, status=204)
