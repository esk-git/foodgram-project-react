from django_filters import rest_framework

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр для модели Ingredient:
    осуществляет поиск по имени ингредиента,
    начиная с первой буквы."""
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для рецептов"""

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = rest_framework.BooleanFilter(
        field_name='favorites__user',
        method='filter_favorites'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name='shopping_cart',
        method='filter_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_favorites(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset
