from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


from . import views

app_name = 'users'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]