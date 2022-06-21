from django.contrib import admin
from django.contrib.admin import display
from django.db.models import Count

from .models import Recipe, Ingredient, Tag, IngredientsForRecipe
from users.models import User, Subscription


class IngredientsForRecipeInline(admin.TabularInline):
    model = IngredientsForRecipe
    min_num = 1
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsForRecipeInline, )
    list_display = ('name', 'author', 'in_favorited')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    ordering = ('-created', )

    @display(description='Добавлений в Избранное:')
    def in_favorited(self, obj):
        queryset = obj.is_favorited.count()
        if queryset:
            return queryset
        return None


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined'
    )
    search_fields = ('first_name', 'email',)
    list_filter = ('username', 'email', 'first_name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(Tag)
