from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from users.serializers import UserReadSerializer

from recipes.models import RecipeInCart, Tag, Recipe, Ingredient, Favorite, IngredientsForRecipe
from .fields import Hex2NameColor
from django.shortcuts import get_object_or_404


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
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientsForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        name = obj.ingredient.name
        return name

    def get_measurement_unit(self, obj):
        measurement_unit = obj.ingredient.measurement_unit
        return measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)
    ingredients = IngredientForRecipeSerializer(many=True, required=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        lookup_field = 'name'

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.is_favorited.filter(user=self.context['request'].user).exists()
        else:
            return 'False'

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.is_in_shopping_cart.filter(user=self.context['request'].user).exists()
        else:
            return 'False'

    def create(self, validated_data):
        ingredients_for_recipe = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(author=self.context.get(
            'request'
        ).user, image=image, **validated_data)
        for ingredient_for_recipe in ingredients_for_recipe:
            ingredient = ingredient_for_recipe.pop('id')
            amount = ingredient_for_recipe.pop('amount')
            IngredientsForRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount,
            )
        recipe.tags.set(tags)
        recipe.save()
        return recipe

    def update(self, pk, validated_data):
        recipe = get_object_or_404(Recipe, id=pk.id)
        if self.context['request'].user == recipe.author:
            ingredients = validated_data.pop('ingredients')
            tags = validated_data.pop('tags')
            recipe.image = validated_data.get('image', recipe.image)
            recipe.name = validated_data.get('name', recipe.name)
            recipe.text = validated_data.get('text', recipe.text)
            recipe.cooking_time = validated_data.get('cooking_time', recipe.cooking_time)
            if ingredients != recipe.ingredients:
                IngredientsForRecipe.objects.filter(recipe=recipe).delete()
                for ingredient in ingredients:
                    id = ingredient.pop('id')
                    amount = ingredient.pop('amount')
                    IngredientsForRecipe.objects.create(
                        recipe=recipe,
                        ingredient=id,
                        amount=amount,
                    )
            if tags != recipe.tags:
                recipe.tags.set(tags)
            recipe.save()
            return recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_id(self, obj):
        id = obj.recipe.id
        return id

    def get_name(self, obj):
        name = obj.recipe.name
        return name

    def get_image(self, obj):
        image = obj.recipe.image
        return f'http://127.0.0.1:8000/'+image.name

    def get_cooking_time(self, obj):
        cooking_time = obj.recipe.cooking_time
        return cooking_time


class RecipeInCartSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = RecipeInCart
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_id(self, obj):
        id = obj.recipe.id
        return id

    def get_name(self, obj):
        name = obj.recipe.name
        return name

    def get_image(self, obj):
        image = obj.recipe.image
        return f'http://127.0.0.1:8000/'+image.name

    def get_cooking_time(self, obj):
        cooking_time = obj.recipe.cooking_time
        return cooking_time
