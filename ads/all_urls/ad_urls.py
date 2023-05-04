from django.urls import path
from ads.views import ad_views

urlpatterns = [
    path('', ad_views.AdListView.as_view(), name='ad_list'),
    path('<int:pk>/', ad_views.AdDetailView.as_view(), name='ad_detail'),
    path('create/', ad_views.AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/update/', ad_views.AdUpdateView.as_view(), name='ad_update'),
    path('<int:pk>/delete/', ad_views.AdDeleteView.as_view(), name='ad_delete'),
    path('<int:pk>/image/', ad_views.AdImageUploadView.as_view(), name='ad_image'),
]
