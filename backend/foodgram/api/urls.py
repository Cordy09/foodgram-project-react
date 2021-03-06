from django.urls import include, path
from rest_framework import routers

from api.views import (FavoriteViewSet, IngredientViewSet, RecipesViewSet,
                       ShoppingCartViewSet, TagsViewSet,
                       download_shopping_cart)

router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')


urlpatterns = [
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_cart'),
    path('', include('users.urls')),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view(
          {'post': 'perform_create', 'delete': 'perform_destroy'}
         ), name='cart'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view(
        {'post': 'perform_create', 'delete': 'perform_destroy'}),
        name='favorite')
]

handler404 = 'api.views.page_not_found'
handler500 = 'api.views.integrity_error'
