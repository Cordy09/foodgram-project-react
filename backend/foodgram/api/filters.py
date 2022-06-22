from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(
        field_name='is_favorited', method='favorite'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='in_carts'
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Recipe
        fields = ('author',)

    def favorite(self, queryset, name, value):
        return queryset.filter(is_favorited__user=self.request.user)

    def in_carts(self, queryset, name, value):
        return queryset.filter(is_in_shopping_cart__user=self.request.user)
