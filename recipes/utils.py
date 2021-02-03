from decimal import Decimal
from django.db import IntegrityError, transaction
from recipes.models import Ingredient, RecipeIngredient, Recipe, Tag


def filter_tag(request):
    '''
    Список рецептов в зависимости от тега
    '''
    tags = request.GET.get('tags', 'bdslt')
    recipe_list = Recipe.objects.prefetch_related(
        'author', 'recipe_tag').filter(recipe_tag__slug__in=tags).distinct()
    return recipe_list, tags


def get_tag(tags):
    tag_dict = {
        'Завтрак': 'b',
        'Обед': 'd',
        'Ужин': 's',
        'Закуски': 'l',
        'Десерт': 't'
    }
    return [tag_dict[item] for item in tags]


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            tags = form.cleaned_data['tag']
            for tag in tags:
                Tag.objects.create(recipe=recipe, title=tag)

            objs = []
            for key, value in form.data.items():
                if 'nameIngredient' in key:
                    title = value
                elif 'valueIngredient' in key:
                    amount = Decimal(value.replace(',', '.'))
                elif 'unitsIngredient' in key:
                    dimension = value
                    ing = Ingredient.objects.get(
                        title=title, dimension=dimension
                    )
                    objs.append(
                        RecipeIngredient(
                            ingredient=ing, recipe=recipe, amount=amount
                        )
                    )
            RecipeIngredient.objects.bulk_create(objs)
            return None
    except IntegrityError:
        return 400


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if 'nameIngredient' in key:
            amount = key.split('_')
            ingredients[name] = int(
                request.POST[f'valueIngredient_{amount[1]}']
            )
    return ingredients
