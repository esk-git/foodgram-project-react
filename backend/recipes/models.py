from constants import (COOKING_TIME_MIN, INGREDIENT_MEASURE_MAX_LEGTH,
                       INGREDIENT_NAME_MAX_LEGTH, RECIPE_NAME_MAX_LENGTH,
                       TAG_COLOR_MAX_LEGTH, TAG_NAME_MAX_LEGTH,
                       TAG_SLUG_MAX_LEGTH)
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов"""
    name = models.CharField(
        'Название тега',
        max_length=TAG_NAME_MAX_LEGTH,
        unique=True,
    )
    color = models.CharField(
        'Цвет тега в HEX',
        max_length=TAG_COLOR_MAX_LEGTH,
        null=True,
        blank=True,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=TAG_SLUG_MAX_LEGTH,
        unique=True,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """Если забыли указать слаг, то присвоить слаг такой же как имя"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    """Модель для ингридиентов"""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=INGREDIENT_NAME_MAX_LEGTH,
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASURE_MAX_LEGTH,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Модель для рецептов"""
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=RECIPE_NAME_MAX_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингрединты'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=COOKING_TIME_MIN
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )
    image = models.ImageField(
        'Фотография блюда',
        upload_to='recipe_images/',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    """Количество ингридиентов"""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В рецептах',
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингридиенты в рецепте",
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    """Избранное"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    def __str__(self) -> str:
        return f'{self.user} добавил в избранное рецепт {self.recipe.name}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('recipe', 'user')


class Cart(models.Model):
    """Корзина"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Ингридиенты в списке покупок'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Список покупок пользователя'
    )

    def __str__(self) -> str:
        return (f'Корзина {self.user} пополнилась '
                f'ингридиентами для {self.recipe.name}')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('recipe', 'user')
