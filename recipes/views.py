from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import requires_csrf_token

from users.models import User

from .common import filter_tag, get_tag, save_recipe
from .forms import RecipeForm
from .models import Recipe


def recipes(request):
    '''
    Cписок рецептов для всех пользователей
    '''
    recipe_list, tags = filter_tag(request)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    template_name = ('indexAuth.html' if request.user.is_authenticated else 'indexNotAuth.html'
    )
    return render(request, template_name, {
            'page': page,
            'paginator': paginator,
            'tags': tags,
        },
    )


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            success_save = save_recipe(request, form)
            if success_save == 400:
                return redirect('page_bad_request')
            return redirect('recipes')
    else:
        form = RecipeForm(request.POST or None)
        tags = []
    return render(request, 'formRecipe.html',
                  {'form': form, 'tags': tags})


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    template_name = (
        'singlePage.html'
        if request.user.is_authenticated
        else 'singlePageNotAuth.html'
    )
    return render(request, template_name, {'recipe': recipe})


def profile(request, username):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(author__username=username)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'authorRecipe.html', {
            'page': page,
            'paginator': paginator,
            'username': username,  # возвращаем обратно пришедший username
            'tags': tags})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe_view', recipe_id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        if form.is_valid():
            recipe.ingredient.remove()
            recipe.recipe_amount.all().delete()
            recipe.recipe_tag.all().delete()
            success_save = save_recipe(request, form)
            if success_save == 400:
                return redirect('page_bad_request')
            return redirect('recipe_view', recipe_id=recipe_id)
    else:
        tags_saved = recipe.recipe_tag.values_list('title', flat=True)
        form = RecipeForm(instance=recipe)
        form.fields['tag'].initial = list(tags_saved)
        tags = get_tag(tags_saved)
    return render(
        request, 'formChangeRecipe.html',
        {'form': form, 'recipe': recipe, 'tags': tags})


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=request.user.username)
    return redirect('recipes')


@login_required
def favorites(request):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(recipe_favorite__user=request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags})


@login_required
def purchases(request):
    recipe_list, tags = filter_tag(request)
    recipe_list = recipe_list.filter(recipe_purchase__user=request.user)
    return render(
        request, 'shopList.html',
        {'recipe_list': recipe_list, 'tags': tags})


@login_required
def subscriptions(request):
    author_list = User.objects.prefetch_related(
        'recipe_author'
            ).filter(
        following__user=request.user)
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'myFollow.html',
        {'page': page, 'paginator': paginator})


def get_ingredients(request):
    ingredient_list = Recipe.objects.prefetch_related(
        'ingredient', 'recipe_amount'
            ).filter(
        recipe_purchase__user=request.user
            ).order_by(
        'ingredient__title'
            ).values(
        'ingredient__title', 'ingredient__dimension'
            ).annotate(
        amount=Sum('recipe_amount__amount'))
    ingredient_txt = [
        (f"\u2022 {item['ingredient__title'].capitalize()} "
         f"({item['ingredient__dimension']}) \u2014 {item['amount']} \n")
        for item in ingredient_list
    ]
    filename = 'ingredients.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@requires_csrf_token
def page_not_found(request, exception):
    return render(request, "error/404.html", {"path": request.path}, status=404)


@requires_csrf_token
def server_error(request):
    return render(request, "error/500.html", status=500)

@requires_csrf_token
def page_bad_request(request, exception):
    return render(request, "error/400.html", {"path": request.path}, status=400)
