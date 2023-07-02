from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, FollowViewSet, RecipeViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('users', FollowViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    # path('users/subscriptions/', FollowViewSet.as_view({'get': 'subscriptions'}), name='user-subscriptions'),
    # path('users/<id>/subscribe/', FollowViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'}), name='user-subscribe'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
