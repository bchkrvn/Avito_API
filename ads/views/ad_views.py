import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.forms import AdCreateForm, AdUpdateForm
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
    form_class = AdCreateForm

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data)

        if form.is_valid():
            ad = Ad()
            form_data = form.cleaned_data
            ad.name = form_data['name']
            ad.price = form_data['price']
            ad.description = form_data['description']
            ad.is_published = form_data['is_published']
            ad.author = form_data['author']
            ad.category = form_data['category']
            ad.save()
            return JsonResponse(ad.json_short(), status=201)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        data = json.loads(request.body)
        form = AdUpdateForm(data=data)

        if form.is_valid():
            ad = self.get_object()
            form_data = form.cleaned_data

            if 'name' in form_data:
                ad.name = form_data['name']
            if 'price' in form_data:
                ad.price = form_data['price']
            if 'description' in form_data:
                ad.description = form_data['description']
            if 'is_published' in form_data:
                ad.is_published = form_data['is_published']
            if 'category' in form_data:
                ad.category = form_data['category']

            ad.save()
            return JsonResponse(ad.json_full(), status=201)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
