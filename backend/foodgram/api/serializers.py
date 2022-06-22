from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Ingredient, IngredientsForRecipe, Recipe,
                            Tag)
from rest_framework import serializers
from users.serializers import UserReadSerializer

from .fields import Hex2NameColor


def is_unique(list):
    id_list = []
    for each in list:
        id_list.append(each.id)
    id_set = set(id_list)
    if len(id_list) == len(id_set):
        return True
    else:
        return False


def create_ingredients_for_recipe(recipe, ingredients_for_recipe):
    ingredients = [
            IngredientsForRecipe(
                recipe=recipe,
                ingredient=each.pop('id'),
                amount=each.pop('amount')
            )
            for each in ingredients_for_recipe]
    IngredientsForRecipe.objects.bulk_create(ingredients)


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True
    )
    name = serializers.CharField(source='ingredient.name', required=False)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', required=False
    )

    class Meta:
        model = IngredientsForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)
    ingredients = IngredientForRecipeSerializer(many=True,
                                                required=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
        lookup_field = 'name'

    def validate_ingredients(self, data):
        ingredients_id = []
        for each in data:
            ingredients_id.append(each['id'])
        if is_unique(ingredients_id):
            return data
        else:
            raise serializers.ValidationError('Поле должно быть уникальным')

    def validate_tags(self, data):
        if is_unique(data):
            return data
        else:
            raise serializers.ValidationError('Поле должно быть уникальным')

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.is_favorited.filter(
                user=self.context['request'].user
            ).exists()
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.is_in_shopping_cart.filter(
                user=self.context['request'].user
            ).exists()
        else:
            return False

    def create(self, validated_data):
        ingredients_for_recipe = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(author=self.context.get(
            'request'
        ).user, image=image, **validated_data)
        create_ingredients_for_recipe(recipe, ingredients_for_recipe)
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        ingredients_for_recipe = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        new_recipe = super().update(recipe, validated_data)
        IngredientsForRecipe.objects.filter(recipe=recipe).delete()
        create_ingredients_for_recipe(new_recipe, ingredients_for_recipe)
        new_recipe.tags.set(tags)
        new_recipe.save()
        return new_recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeInfoSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        required=True
    )
    name = serializers.CharField()
    image = serializers.ImageField()
    cooking_time = serializers.CharField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
