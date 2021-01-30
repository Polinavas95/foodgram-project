from django.db import models

from users.models import User


class Tag(models.Model):
    COLOR = {
        'завтрак': 'оранжевый',
        'обед': 'оранжевый',
        'ужин': 'оранжевый',
        'перекус': 'зеленый',
        'десерт': 'фиолетовый'
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

    def __str__(self):
        return self.title

    def _generate_color_and_slug(self):
        value = self.title
        self.color = self.COLOR[value]
        self.slug = self.SLUG[value]

    def save(self, *args, **kwargs):
        self._generate_color_and_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название')
    dimension = models.CharField(max_length=200, verbose_name='Eдиница измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_author', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipe_ingredient',
        verbose_name='Ингридиенты')
    tag = models.ManyToManyField(Tag, related_name='recipe_tag', verbose_name='Тег')
    duration = models.IntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    @property
    def favorite_count(self):
        return self.recipe_amount.count()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class RecipeIngredient(models.Model):
    """
    Показывает количество ингридиента, необходимое для данного рецепта
    """
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_amount', verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт - Ингредиент'
        verbose_name_plural = 'Рецепты - Ингредиенты'
