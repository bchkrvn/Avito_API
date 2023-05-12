from django.urls import path, include

urlpatterns = [
    path('categories/', include('ads.all_urls.category_urls')),
    path('ads/', include('ads.all_urls.ad_urls')),
    path('users/', include('ads.all_urls.user_urls')),
    path('locations/', include('ads.all_urls.location_urls')),
]
