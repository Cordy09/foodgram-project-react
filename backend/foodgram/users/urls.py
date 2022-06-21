from django.urls import include, path
from rest_framework import routers
from .views import SubscriptionsViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('users/<int:user_id>/subscribe/', SubscriptionsViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='subscribe'
    ),
    path('users/subscriptions/', SubscriptionsViewSet.as_view(
        {'get': 'list'}), name='subscriptions'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
