from django.urls import path

from api import views

urlpatterns = [
    path("v1/ingredients/", views.IngredientAPIView.as_view()),
    path("v1/favorites/", views.FavoriteCreateView.as_view()),
    path("v1/favorites/<int:recipe_id>/", views.FavoriteDeleteView.as_view()),
    path("v1/purchases/", views.PurchaseCreateView.as_view()),
    path("v1/purchases/<int:recipe_id>/", views.PurchaseDeleteView.as_view()),
    path("v1/subscriptions/", views.SubscribeCreateView.as_view()),
    path("v1/subscriptions/<int:author_id>/", views.SubscribeDeleteView.as_view()),
]
