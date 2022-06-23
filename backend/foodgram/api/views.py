from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, RecipeInCart, Tag

from .filters import RecipeFilter
from .mixins import CreateDestroy, RetrieveListViewSet
from .permissions import IsRecipeOwnerOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


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


class FavoriteViewSet(CreateDestroy):
    queryset = Favorite.objects.all()


class ShoppingCartViewSet(CreateDestroy):
    queryset = RecipeInCart.objects.all()


@api_view(['GET'])
def download_shopping_cart(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(is_in_shopping_cart__user=request.user)
        ingredients = recipes.values(
            'ingredients__ingredient__name',
            'ingredients__ingredient__measurement_unit'
        ).order_by('name').annotate(
            total_amount=Sum('ingredients__amount'))
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


def page_not_found(request, exception):
    return render(request, {'path': request.path}, status=404)


def integrity_error(request):
    return render(request, {'path': request.path}, status=400)
