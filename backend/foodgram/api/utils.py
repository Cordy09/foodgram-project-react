from recipes.models import IngredientsForRecipe


def is_unique(list):
    id_list = []
    for each in list:
        id_list.append(each.id)
    id_set = set(id_list)
    return len(id_list) == len(id_set)


def create_ingredients_for_recipe(recipe, ingredients_for_recipe):
    ingredients = [
            IngredientsForRecipe(
                recipe=recipe,
                ingredient=each.pop('id'),
                amount=each.pop('amount')
            )
            for each in ingredients_for_recipe]
    IngredientsForRecipe.objects.bulk_create(ingredients)
