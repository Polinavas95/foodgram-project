from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    """
    Форма для создания новых рецептов
    """

    TAG_CHOICES = (
        ("Завтрак", "b"),
        ("Обед", "d"),
        ("Ужин", "s"),
        ("Закуски", "l"),
        ("Десерты", "t"),
    )
    tag = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=TAG_CHOICES
    )
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form__textarea"}))

    class Meta:
        model = Recipe
        fields = ("title", "duration", "text", "image")
