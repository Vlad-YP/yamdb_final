import uuid

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title
from users.models import User
from users.send_mail_util import send_confirmation_mail

from .filters import TitleSearchFilter
from .permissions import (AdminOnly, AdminOrReadOnly,
                          AuthorAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, LoginSerializer, ReviewSerializer,
                          SignupUserSerializer, TitleSerializer,
                          UserMeSerializer, UsersSerializer)


class CreateRetrieveDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    """Вьюсет для модели категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(CreateRetrieveDestroyViewSet):
    """Вьюсет для модели жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тайтлов."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    filterset_class = TitleSearchFilter
    filterset_fields = ['genre', 'category', 'name', 'year']
    permission_classes = (AdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ревью."""
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев."""
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    """Регистрация юзера и получение кода для api."""
    serializer = SignupUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        obj_user, created = User.objects.get_or_create(
            email=email,
            username=username
        )
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    generated_uuid = str(uuid.uuid4())
    obj_user.confirmation_code = generated_uuid
    obj_user.save()
    send_confirmation_mail(email, generated_uuid)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated, AdminOnly)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username')
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,))
    def administration_user_me(self, request):
        me_user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(me_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(
            me_user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_generate(request):
    """Функция формирования токена."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
