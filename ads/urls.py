from django.urls import path, include

urlpatterns = [
    path('categories/', include('ads.all_urls.category_urls')),
]
