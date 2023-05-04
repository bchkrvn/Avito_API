import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.forms import ValidationError

from ads.forms import AdForm
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
        print(ad)

        response = {
            'name': ad.name,
            'author': ad.author.json_short(),
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url,
            'category': ad.category.json(),
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    form_class = AdForm

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = form.clean_author()
            ad.category = form.clean_category()
            ad.save()
            return JsonResponse(ad.json_short(), status=201)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)

        # except ValidationError as e:
        #     return JsonResponse({'error': e.message}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    form_class = AdForm

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data, instance=self.get_object())

        if form.is_valid():
            category = form.save()
            return JsonResponse(category.json(), status=204)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
