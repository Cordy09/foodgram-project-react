from django.urls import include, path
# from .views import TagsViewSet
from rest_framework import routers


from api.views import (TagsViewSet, RecipesViewSet,
                       SubscriptionViewSet, IngredientViewSet, FavoriteViewSet)

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')
router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [

    path('', include(router.urls)),
    path('', include('users.urls')),
]
