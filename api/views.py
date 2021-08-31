from django.contrib.auth import get_user_model
from django.db import models
from django.http import Http404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import GenreCategoryFilter
from api.permissions import SimpleResourceUsage, IsAdminOrReadOnly, \
    IsCustomAdminUser
from api.serializers import *
from api.models import Title, Review, Comment, Category, Genre

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """Title for admin create/edit or user read only"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = GenreCategoryFilter
    search_fields = ['genre__slug']

    def get_queryset(self):
        return Title.objects.all().annotate(rating=models.Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        else:
            return self.serializer_class


class ReviewViewSet(viewsets.ModelViewSet):
    """Class for Review model actions"""
    serializer_class = ReviewSerializer
    permission_classes = [SimpleResourceUsage]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_object(self):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, review)
        return review

    def get_queryset(self):
        if not Title.objects.filter(id=self.kwargs['title_pk']).exists():
            raise Http404()
        return Review.objects.filter(title_id=self.kwargs['title_pk'])

    def perform_create(self, serializer):
        if not Title.objects.filter(id=self.kwargs['title_pk']).exists():
            raise Http404()
        if Review.objects.filter(author=self.request.user,
                                 title=Title.objects.get(
                                     id=self.kwargs['title_pk'])).exists():
            raise ValidationError
        serializer.save(title=Title.objects.get(id=self.kwargs['title_pk']),
                        author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        else:
            return self.serializer_class


class CommentViewSet(viewsets.ModelViewSet):
    """Class for Review model actions"""
    serializer_class = CommentSerializer
    permission_classes = [SimpleResourceUsage]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_queryset(self):
        if not Review.objects.filter(id=self.kwargs['review_pk'],
                                     title_id=self.kwargs['title_pk']).exists():
            raise Http404()
        return Comment.objects.filter(review_id=self.kwargs['review_pk'],
                                      review__title_id=self.kwargs['title_pk'])

    def perform_create(self, serializer):
        if not Review.objects.filter(id=self.kwargs['review_pk'],
                                     title_id=self.kwargs['title_pk']).exists():
            raise Http404()
        serializer.save(review=Review.objects.get(id=self.kwargs['review_pk']),
                        author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        else:
            return self.serializer_class


class UsersViewSet(viewsets.ModelViewSet):
    """Class for User model actions, AdminOnly"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCustomAdminUser]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        else:
            return self.serializer_class


class UserSelfProfileView(APIView):  # APIView because url dont have PK
    """Edit user's profile by himself"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, email=self.request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, email=self.request.user.email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateDestroyViewSet(mixins.ListModelMixin,
                                       mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    """Class for Category model actions, AdminOnly"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'


class GenreListCreateDestroyViewSet(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """Class for Genre model actions, AdminOnly"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'

