from django.shortcuts import get_object_or_404
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe
from users.models import User

from api.models import Favorite, Purchase, Subscribe
from api.serializers import (
    FavoriteSerializer, SubscribeSerializer,
    IngredientSerializer, PurchaseSerializer
)


class IngredientAPIView(generics.ListAPIView):
    """Класс для поиска в базе ингредиентов по их названиям."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


class FavoriteCreateView(generics.CreateAPIView):
    """Класс для добавления рецепта в избранное."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class FavoriteDeleteView(APIView):
    """Класс для удаления рецепта из избранного."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = recipe.recipe_favorite.filter(user=request.user)
        if favorite.delete():
            return Response({"success": True})
        return Response({"success": False})


class PurchaseCreateView(generics.CreateAPIView):
    """Класс для добавления рецепта в список покупок."""
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class PurchaseDeleteView(APIView):
    """Класс для удаления рецепта из списка покупок."""
    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = recipe.recipe_purchase.filter(user=request.user)
        if purchase.delete():
            return Response({"success": True})
        return Response({"success": False})


class SubscribeCreateView(generics.CreateAPIView):
    """Класс для добавления автора в подписку."""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True})
        return Response({"success": False})


class SubscribeDeleteView(APIView):
    """Класс для удаления автора из подписки."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        follow = author.following.filter(user=request.user)
        if follow.delete():
            return Response({"success": True})
        return Response({"success": False})
