from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название', blank=False)
    duration = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    text = models.TextField(verbose_name='Описание', blank=False)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    ingredient = models.ManyToManyField('Ingredient', through='RecipeIngredient', related_name='recipe_ingredient',
        verbose_name='Ингридиенты')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    @property
    def favorite_count(self):
        return self.recipe_amount.count()

    def image_img(self):
        if self.image:
            return mark_safe(f'<img width="90" height="50" src="{self.image.url}" />')
            return 'Без изображения'

    image_img.short_description = 'изображение'


class Tag(models.Model):
    COLOR = {
        'завтрак': 'orange',
        'обед': 'orange',
        'ужин': 'orange',
        'перекус': 'green',
        'десерт': 'purple'
    }
    SLUG = {
        'завтрак': 'b',
        'обед': 'd',
        'ужин': 's',
        'перекус': 'l',
        'десерт': 't',
    }
    TITLE = (
        ('завтрак', 'завтрак'),
        ('обед', 'обед'),
        ('ужин', 'ужин'),
        ('перекус', 'перекус'),
        ('десерт', 'десерт')
    )

    title = models.CharField(max_length=50, choices=TITLE, verbose_name='Название')
    color = models.CharField(max_length=50, editable=False, verbose_name='Цвет')
    slug = models.SlugField(max_length=50, editable=False, verbose_name='Адрес')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='рецепт', related_name='recipe_tag')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title

    def _generate_color_and_slug(self):
        value = self.title
        self.color = self.COLOR[value]
        self.slug = self.SLUG[value]
        print('value', value)
        print('color', self.COLOR[value])
        print('slug', self.SLUG[value])

    def save(self, *args, **kwargs):
        self._generate_color_and_slug()
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    title = models.CharField(max_length=200, db_index=True, unique=True, verbose_name='Название')
    dimension = models.CharField(max_length=200, verbose_name='Eдиница измерения')

    def __str__(self):
        return f'{self.title}, {self.dimension}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """
    Показывает количество ингридиента, необходимое для данного рецепта
    """
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(1)], verbose_name='Количество')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_amount', verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт - Ингредиент'
        verbose_name_plural = 'Рецепты - Ингредиенты'

    def __str__(self):
        return f'Из рецепта "{self.recipe}"'
