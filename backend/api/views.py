import io
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters
from reportlab.pdfgen import canvas

from api.permissions import AuthorOrReadOnly
from recipes.models import (Tag, Recipe, Ingredient,
                            RecipeIngredient, Favorite, Cart)
from api.filters import IngredientFilter, RecipeFilter
from api.serializers import (TagSerializer, FollowSerializer,
                             IngredientSerializer, RecipeSerializer,
                             RecipeListSerializer, RecipeForFollowSerializer)
from users.models import User, Follow


class FollowViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = request.user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if user == author:
            return Response({'message': 'Вы не можете подписаться на себя'})

        message = ''

        if request.method == 'POST':
            if Follow.objects.filter(user=self.request.user,
                                     author=author).exists():
                return Response(
                    {'errors': f'Вы уже подписаны на {author}'})
            queryset = Follow.objects.create(user=self.request.user,
                                             author=author)
            serializer = FollowSerializer(queryset,
                                          context={'request': request})
            return Response(serializer.data)
        elif request.method == 'DELETE':
            Follow.objects.filter(user=user, author=author).delete()
            message = f'Вы отписались от {author}'

        return Response({'message': message})


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    # permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'rerieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_obj(Favorite, recipe, request.user)
        return self.delete_obj(Favorite, recipe, request.user)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_obj(Cart, recipe, request.user)
        return self.delete_obj(Cart, recipe, request.user)

    def add_obj(self, model, recipe, user):
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': 'Уже добавлен'}
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeForFollowSerializer(recipe)
        return Response(serializer.data)

    def delete_obj(self, model, recipe, user):
        if model.objects.filter(user=user, recipe=recipe).exists():
            model.objects.filter(user=user, recipe=recipe).delete()
            return Response(
                {'succesfully': 'Удален'}
            )
        return Response({'errors': 'Отсутствует в списке'})

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart = Cart.objects.filter(user=request.user)
        recipe_ids = shopping_cart.values_list('recipe_id', flat=True)
        ingredients = RecipeIngredient.objects.filter(recipe__in=recipe_ids)
        ingredient_dict = {}
        for ingredient in ingredients:
            key = (ingredient.ingredient.name,
                   ingredient.ingredient.measurement_unit)
            if key in ingredient_dict:
                ingredient_dict[key] += ingredient.amount
            else:
                ingredient_dict[key] = ingredient.amount

        buffer = io.BytesIO()

        p = canvas.Canvas(buffer)
        p.setFont('Helvetica', 12)
        p.drawString(100, 100, "Список покупок")

        y = 120
        for ingredient, amount in ingredient_dict.items():
            name, unit = ingredient
            ingredient_line = f"{name}: {amount} {unit}"
            p.drawString(100, y, ingredient_line)
            y += 20

        p.showPage()
        p.save()

        buffer.seek(0)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"'
        )
        response.write(buffer.getvalue())

        return response
