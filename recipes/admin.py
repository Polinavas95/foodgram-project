from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)


class RecipeIngredient(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('favorite_count',)
    list_display = ('title', 'author')
    list_filter = ('title', 'author', 'tag')
    inlines = (RecipeIngredient,)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
