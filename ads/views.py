import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.forms import AdForm, CategoryForm
from ads.models import Category, Ad


def ok_view(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class CategoriesView(View):

    def get(self, request):
        categories = Category.objects.all()
        response = [category.json() for category in categories]
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        form = CategoryForm(data=data)

        if form.is_valid():
            category = form.save()
            return JsonResponse(category.json())
        else:
            return JsonResponse({'error': 'Bad Request'}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().json())


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):

    def get(self, request):
        ads = ADS.objects.all()
        response = [ad.json_short() for ad in ads]
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        form = AdForm(data=data)

        if form.is_valid():
            ad = form.save()
            return JsonResponse(ad.json_short())
        else:
            return JsonResponse({'error': 'Bad Request'}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().json_full())

