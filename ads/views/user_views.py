import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from ads.models import User, Location
from ads.serializers.user_serializer import UserSerializers


class UserListView(ListAPIView):
    model = User
    queryset = User.objects.prefetch_related('locations').annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username').all()

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.get_queryset(), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        try:
            users = paginator.page(page_number)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            users = paginator.page(1)

        items = [
            {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'age': user.age,
                'total_ads': user.total_ads,
            } for user in users
        ]

        response = {
            "items": items,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User
    queryset = User.objects.prefetch_related('locations').annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username')

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        response = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'age': user.age,
            'location': user.location.json(),
            'total_ads': user.total_ads,
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            user = User()
            user.first_name = data.get('first_name', None)
            user.last_name = data.get('last_name', None)
            user.username = data.get('username', None)
            user.password = data.get('password', None)
            user.role = data.get('role', None)
            user.age = data.get('age', None)
            user.location, _ = Location.objects.get_or_create(**data.get('location'))

            user.save()

            response = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'age': user.age,
                'location': user.location.json(),
            }
            return JsonResponse(response, status=201)
        except (KeyError, ValidationError):
            return JsonResponse({'error': f'Wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            user = self.get_object()
            if 'first_name' in data:
                user.first_name = data.get('first_name')
            if 'last_name' in data:
                user.last_name = data.get('last_name')
            if 'username' in data:
                user.username = data.get('username')
            if 'password' in data:
                user.password = data.get('password')
            if 'role' in data:
                user.role = data.get('role')
            if 'age' in data:
                user.age = data.get('age')
            if 'location' in data:
                user.location, _ = Location.objects.get_or_create(**data.get('location'))

            user.save()

            response = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'age': user.age,
                'location': user.location.json(),
            }
            return JsonResponse(response, status=201)

        except ValidationError:
            return JsonResponse({'error': f'Wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


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
