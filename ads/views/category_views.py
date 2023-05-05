import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.forms import CategoryForm
from ads.models import Category


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.get_queryset().order_by('name'), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        try:
            categories = paginator.page(page_number)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            categories = paginator.page(1)

        response = {
            "items": [category.json() for category in categories],
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().json())


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data)

        if form.is_valid():
            category = form.save()
            return JsonResponse(category.json(), status=201)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data, instance=self.get_object())

        if form.is_valid():
            category = form.save()
            return JsonResponse(category.json(), status=204)
        else:
            return JsonResponse({'error': 'wrong data'}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
