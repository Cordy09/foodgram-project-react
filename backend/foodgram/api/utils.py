from recipes.models import IngredientsForRecipe, Ingredient


def is_unique(list):
    id_set = set(list)
    return len(list) == len(id_set)


def create_ingredients_for_recipe(recipe, ingredients_for_recipe):
    ingredients = [
            IngredientsForRecipe(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=each['ingredient']['id']),
                amount=each['amount']
            )
            for each in ingredients_for_recipe]
    IngredientsForRecipe.objects.bulk_create(ingredients)
