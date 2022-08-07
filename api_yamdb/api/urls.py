from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, CommentViewSet,
    ReviewViewSet, UsersViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
