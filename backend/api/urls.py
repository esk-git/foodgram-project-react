from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (FollowViewSet, IngredientViewSet,
                       RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('users', FollowViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
