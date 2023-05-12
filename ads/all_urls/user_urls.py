from django.urls import path, include
from rest_framework import routers

from ads.views import user_views

router = routers.SimpleRouter()
router.register('new_user', user_views.UsersGenericViewSet)

urlpatterns = [
    path('', user_views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/', user_views.UserDetailView.as_view(), name='user_detail'),
    path('create/', user_views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', user_views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', user_views.UserDeleteView.as_view(), name='user_delete'),
    path('', include(router.urls)),
]