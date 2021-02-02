from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from users.models import User

from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.utils import filter_tag, get_tag, save_recipe


@cache_page(20, key_prefix='index_page')
def index(request):
    recipe_list, tags = filter_tag(request)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags, }
    print('recipe_list', recipe_list)
    print('tags', tags)
    template_name = ('indexAuth.html' if request.user.is_authenticated else 'indexNotAuth.html')

    return render(request, template_name, context)


def profile(request, username):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(author__username=username)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'username': username, 'tags': tags, }
    return render(request, 'authorRecipe.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    template_name = ('singlePage.html' if request.user.is_authenticated else 'singlePageNotAuth.html')
    return render(request, template_name, {'recipe': recipe})


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            success_save = save_recipe(request, form)
            if success_save == 400:
                print('400 form', form)
                return redirect('page_bad_request')
            return redirect('index')
    form = RecipeForm(request.POST or None)
    tags = []
    context = {'form': form, 'tags': tags}
    print('else form', form)
    print('else tags', tags)
    return render(request, 'formRecipe.html', context)


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
        if form.is_valid():
            recipe.ingredient.remove()
            recipe.recipe_amount.all().delete()
            recipe.recipes_tag.all().delete()
            success_save = save_recipe(request, form)
            if success_save == 400:
                return redirect('page_bad_request')
            return redirect('recipe_view', recipe_id=recipe_id)
    tags_saved = recipe.tag.values_list('title', flat=True)
    form = RecipeForm(instance=recipe)
    form.fields['tag'].initial = list(tags_saved)
    tags = get_tag(tags_saved)
    context = {'form': form, 'recipe': recipe, 'tags': tags}
    return render(request, 'formChangeRecipe.html', context)


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=request.user.username)
    return redirect('index')


@login_required
def favorites(request):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(recipe_favorite__user=request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags}
    return render(request, 'favorite.html', context)


@login_required
def purchases(request):
    """
     Отображение списка покупок
    """
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(recipe_purchase__user=request.user)
    context = {'recipe_list': recipe_list, 'tags': tags}
    return render(request, 'shopList.html', context)


@login_required
def subscriptions(request):
    author_list = User.objects.prefetch_related('recipe_author').filter(following__user=request.user)
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'myFollow.html', context)


def download(request):
    """
     Отправление файла с ингредиентами
    """
    ingredient_list = Recipe.objects.prefetch_related('ingredient', 'recipe_amount').filter(
        recipe_purchase__user=request.user).order_by('ingredient__title').values(
        'ingredient__title', 'ingredient__dimension').annotate(amount=Sum('recipe_amount__amount'))
    ingredient_txt = [(f'\u2022 {item["ingredient__title"].capitalize()} '
                       f'({item["ingredient__dimension"]}) \u2014 {item["amount"]} \n')
                      for item in ingredient_list]
    filename = 'ingredients.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def page_bad_request(request, exception):
    return render(request, 'error/400.html', {'path': request.path}, status=400)


def page_not_found(request, exception):
    return render(request, 'error/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'error/500.html', status=500)
