import django_filters
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Favorite, Purchase, Subscribe
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    SubscribeSerializer,
)
from recipes.models import Ingredient

from .permissions import FoodgramPermission


class PerformCreateMixin:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, FoodgramPermission)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class IngredientViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, FoodgramPermission)
    filter_backends = [filters.SearchFilter]
    search_fields = ["^title"]


class PurchaseViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscribeViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (FoodgramPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ["=user__username", "=following__username"]
