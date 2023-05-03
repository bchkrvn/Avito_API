from django.urls import path
from ads.views import category_views

urlpatterns = [
    path('', category_views.CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/', category_views.CategoryDetailView.as_view(), name='category_detail'),
    path('create/', category_views.CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/update/', category_views.CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/delete/', category_views.CategoryDeleteView.as_view(), name='category_delete'),
]
