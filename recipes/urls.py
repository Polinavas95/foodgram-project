from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes, name='index'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('recipes/<username>/', views.profile, name='profile'),
    path('recipes/', views.recipes, name='recipes'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('shoplist/', views.get_ingredients, name='shoplist'),
    # path('card/download_card', views.download_card, name='download_card'),
    # path('card', views.CardView.as_view(), name='card'),
]