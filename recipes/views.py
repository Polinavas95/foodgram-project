from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import RecipeForm
from .mixins import RecipeObjectMixin, AuthorRequiredMixin
from .models import Recipe, User, ShoppingList, FollowUser, FollowRecipe


class IndexView(RecipeObjectMixin, ListView):
    queryset = Recipe.objects.select_related('author').prefetch_related('tags')
    context_object_name = 'recipes'
    ordering = ['-pub_date']
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        filters = self.request.GET.getlist('filters')

        if filters:
            qs = qs.filter(tags__slug__in=filters).distinct()
        return qs

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['indexAuth .html']
        return ['indexNotAuth.html']


class RecipeCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'formRecipe.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Показывает страницу только что созданного рецепта
        return reverse_lazy('recipe_page', kwargs={'pk': self.object.pk})


class RecipeDetailView(RecipeObjectMixin, DetailView):
    model = Recipe
    context_object_name = 'recipe'

    def get_template_names(self):
        # показывать разные шаблоны в зависимости от залогинен ли пользователь
        if self.request.user.is_authenticated:
            return ['recipePage.html']
        return ['singlePage.html']


class FavoriteView(LoginRequiredMixin, RecipeObjectMixin, ListView):
    template_name = 'favorite.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        qs = FollowRecipe.objects.select_related('user', 'recipe').filter(
            user=self.request.user).order_by('-recipe__pub_date')
        filters = self.request.GET.getlist('filters')

        if filters:
            qs = qs.filter(recipe__tags__slug__in=filters).distinct()
        return qs


class ProfileView(RecipeObjectMixin, ListView):
    template_name = 'authorRecipe.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        username = self.kwargs.get('username')
        qs = Recipe.objects.select_related('author').prefetch_related('tags', 'ingredients').filter(
            author__username=username).order_by('-pub_date')
        filters = self.request.GET.getlist('filters')
        if filters:
            qs = qs.filter(tags__slug__in=filters).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(User, username=self.kwargs.get('username'))

        return context


class FollowView(LoginRequiredMixin, ListView):
    template_name = 'myFollow.html'
    context_object_name = 'following'
    paginate_by = 3

    def get_queryset(self):
        qs = FollowUser.objects.select_related('user', 'author').filter(user=self.request.user)
        return qs


class CardView(LoginRequiredMixin, ListView):
    template_name = 'shopList.html'
    context_object_name = 'card'

    def get_queryset(self):
        qs = ShoppingList.objects.select_related('user', 'recipe').filter( user=self.request.user)
        return qs


class RecipeEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'formChangeRecipe.html'

    def get_success_url(self):
        return reverse_lazy('recipe_page', kwargs={'pk': self.kwargs['pk']})


class RecipeDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    template_name = 'recipe_confirm_delete.html'
    model = Recipe
    success_url = reverse_lazy('indexAuth')


@login_required
def download_card(request):
    recipes = Recipe.objects.filter(shopping_list__user=request.user)
    ingredients = recipes.values('ingredients__title', 'ingredients__dimension').annotate(
        Sum('recipe_ingredients__amount'))
    file_data = ''

    # Все ингридиенты вида ['молоко', 'мл', 150] парсируются в str и конкатируются в пустой файл с переносом строки
    for item in ingredients:
        line = ' '.join(str(value) for value in item.values())
        file_data += line + '\n'

    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
