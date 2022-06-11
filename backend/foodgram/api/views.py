from recipes.models import Tag, Recipe, Ingredient, Subscription, Favorite
from rest_framework import viewsets
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, SubscriptionSerializer, FavoriteSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ('title', 'slug')
    # lookup_field = 'slug'


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
