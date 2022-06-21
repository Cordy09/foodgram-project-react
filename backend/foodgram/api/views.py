from .permissions import IsRecipeOwnerOrReadOnly
from .filters import RecipeFilter
from recipes.models import Tag, Recipe, Ingredient, Favorite, RecipeInCart
from rest_framework import viewsets
from .serializers import (TagSerializer, RecipeSerializer,
                          IngredientSerializer,
                          FavoriteSerializer,
                          RecipeInCartSerializer)
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import RetrieveListViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import (AllowAny, IsAuthenticated)


class TagsViewSet(RetrieveListViewSet):

    permission_classes = [AllowAny]

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [IsRecipeOwnerOrReadOnly]


class IngredientViewSet(RetrieveListViewSet):

    search_fields = ('^name',)

    def list(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        ingredient = get_object_or_404(queryset, pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete']

    def perform_create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                recipe_id=recipe.id, user=self.request.user
            )
            return Response(serializer.data)

    def perform_destroy(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            Favorite.objects.get(recipe=recipe, user=request.user).delete()
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = RecipeInCart.objects.all()
    serializer_class = RecipeInCartSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'delete']

    def perform_create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = RecipeInCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                recipe=recipe, user=self.request.user
            )
            return Response(serializer.data)

    def perform_destroy(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            RecipeInCart.objects.get(recipe=recipe, user=request.user).delete()
        except RecipeInCart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(is_in_shopping_cart__user=request.user)
        ingredients = recipes.values(
            'ingredients__ingredient__name',
            'ingredients__ingredient__measurement_unit'
        ).order_by('name').annotate(
            total_amount=Sum('ingredients__amount')).all()
        text = 'Список покупок:\n'
        for number, ingredient in enumerate(ingredients, start=1):
            amount = ingredient['total_amount']
            name = ingredient['ingredients__ingredient__name']
            measure_unit = ingredient[
                'ingredients__ingredient__measurement_unit']
            text += (
                f'{number}. '
                f'{name} - '
                f'{amount} '
                f'{measure_unit}\n'
            )
        response = HttpResponse(text, content_type='text/plain')
        filename = 'shopping_list.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return HttpResponse(text, content_type='text/plain')
    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
