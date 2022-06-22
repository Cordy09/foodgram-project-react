from recipes.models import Recipe
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'is_subscribed', 'id')
        model = User

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            caller = self.context['request'].user
            return obj.publishers.filter(user=caller).exists()
        return False


class SetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        fields = (
            'new_password', 'current_password')
        model = User


class SubscriptionRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count')
        model = User

    def get_is_subscribed(self, obj):
        caller = self.context['request'].user
        return obj.publishers.filter(user=caller).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        serializer = SubscriptionRecipeSerializer(recipes, many=True)
        self.context.update({'recipes_count': len(serializer.data)})
        return serializer.data

    def get_recipes_count(self, obj):
        return self.context['recipes_count']
