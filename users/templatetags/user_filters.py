from django import template

from api.models import Favorite, Purchase, Subscribe

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_subscribe(value, user):
    return Subscribe.objects.filter(author=value, user=user).exists()


@register.filter
def is_favorite(value, user):
    return Favorite.objects.filter(recipe=value, user=user).exists()


@register.filter
def is_purchase(value, user):
    return Purchase.objects.filter(recipe=value, user=user).exists()
