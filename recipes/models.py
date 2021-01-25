from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    quantity = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField()
    time_for_preparing = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    @property
    def favorite_amount(self):
        return self.recipe_followers.count()

    @property
    def description_as_list(self):
        return self.description.split('\n')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipes')
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient.title} - {self.amount} ({self.ingredient.quantity})'

    class Meta:
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shopping_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopping_list')

    def __str__(self):
        return f'Пользователь: {self.user} добавил в список покупок ингридиенты из рецепта "{self.recipe}"'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'Пользователь: {self.user} подписался на "{self.author}"'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class FollowRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_followers')

    def __str__(self):
        return f'Пользователь: {self.user} добавил в избранное рецепт "{self.recipe}"'

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


def is_following(self, user):
    """
    Метод для поиска пользователя среди подписчиков
    """
    return self.following.filter(user=user).exists()


# Добавление метода для модели User на проверку наличия его среди подписчиков
User.add_to_class('is_following', is_following)
