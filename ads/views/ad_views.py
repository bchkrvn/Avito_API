import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad


class AdListView(ListView):
    model = Ad
    queryset = Ad.published.all()

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.get_queryset(), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        try:
            ads = paginator.page(page_number)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            ads = paginator.page(1)

        response = {
            "items": [ad.json_short() for ad in ads],
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad
    queryset = Ad.published.select_related('author').select_related('category')

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        response = {
            'name': ad.name,
            'author': ad.author.json_short(),
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category': ad.category.json(),
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            ad = Ad()
            ad.name = data['name']
            ad.price = data['price']
            ad.description = data['description']
            ad.is_published = data['is_published']
            ad.author_id = data['author_id']
            ad.category_id = data['category_id']
            ad.save()
            return JsonResponse(ad.json_short(), status=201)

        except (KeyError, ValidationError):
            return JsonResponse({'error': f'Wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        data = json.loads(request.body)

        try:
            ad = Ad()
            if 'name' in data:
                ad.name = data['name']
            if 'price' in data:
                ad.price = data['price']
            if 'description' in data:
                ad.description = data['description']
            if 'is_published' in data:
                ad.is_published = data['is_published']
            if 'author_id' in data:
                ad.author_id = data['author_id']
            if 'category_id' in data:
                ad.category_id = data['category_id']
            ad.save()
            return JsonResponse(ad.json_short(), status=201)

        except ValidationError:
            return JsonResponse({'error': f'Wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageUploadView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        img = request.FILES['image']
        img.name = f'post{ad.id}.jpg'
        ad.image = img
        ad.save()

        return JsonResponse({'id': ad.id, 'image': ad.image.url})


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
