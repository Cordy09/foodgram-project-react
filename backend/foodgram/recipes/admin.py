from django.contrib import admin

from .models import Recipe, Ingredient, Subscription, Tag
from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    # def show_saving(self, obj):
    #     saving = Recipe.objects.filter().count()


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(Tag)
