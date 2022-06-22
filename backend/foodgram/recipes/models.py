from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=30, verbose_name='Единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name='Название тэга')
    slug = models.SlugField(unique=True, verbose_name='Slug тэга')
    color = models.CharField(
        max_length=7, default="#ffffff",
        verbose_name='Цвет тэга', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag, related_name='recipes',
        verbose_name='Тэги', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Название рецепта', max_length=200)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        blank=True, null=True,
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.IntegerField(
            verbose_name='Время приготовления',
            validators=[MinValueValidator(
                1, message='Время приготовления должно быть больше'
            )])
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text


class IngredientsForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='Ингредиент', related_name='recipes')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    amount = models.IntegerField(
            validators=[MinValueValidator(
                1, message='Количество должно быть больше'
            )])

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_recipe_ingredient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]


class RecipeInCart(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='is_in_shopping_cart',
        verbose_name='Рецепт в списке покупок',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name='carts',
        verbose_name='Владелец списка покупок',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='one_recipe_in_cart'
            )
        ]
