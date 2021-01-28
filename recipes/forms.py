from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    '''
    Форма для создания рецепта
    '''
    TAG_CHOICES = (
        ('Завтрак', 'orange'),
        ('Обед', 'orange'),
        ('Ужин', 'orange'),
        ('Перекус', 'green'),
        ('Десерты', 'purple')
    )

    title = forms.CharField(max_length=256)
    tag = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=TAG_CHOICES,
    )
    duration = forms.IntegerField(min_value=1)
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form__textarea'})
    )
    image = forms.ImageField()

    class Meta:
        model = Recipe
        fields = ('title', 'duration', 'text', 'image', )
