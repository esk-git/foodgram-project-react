from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов"""
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'Цвет тега в HEX',
        max_length=7,
        null=True,
        blank=True,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """Если забыли указать слаг, то присвоить слаг такойже как имя"""
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
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерение'
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
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг'
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
        default=1
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


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

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('recipe', 'user')
