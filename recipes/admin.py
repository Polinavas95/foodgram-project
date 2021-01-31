from django.contrib import admin
from django.db.models import Count
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAmountInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 0
    verbose_name = 'ингредиент'


class TagInline(admin.TabularInline):
    model = Tag
    min_num = 1
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInline, TagInline)
    list_display = ('id', 'title', 'author', 'image_img', 'duration', 'get_tag',)
    list_filter = ('author', 'recipe_tag__title', )
    search_fields = ('title', 'author__username', )
    autocomplete_fields = ('author', )
    ordering = ('-pub_date', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_get_favorite=Count('recipe_favorite'))

    def get_tag(self, obj):
        return list(obj.recipe_tag.values_list('title', flat=True))

    get_tag.short_description = 'теги'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'dimension', )
    search_fields = ('^title', )


@admin.register(RecipeIngredient)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'recipe', )
