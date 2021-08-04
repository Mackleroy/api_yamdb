from django.urls import path, include
from rest_framework_nested import routers

from api.views import *

title_router = routers.SimpleRouter()
title_router.register('titles', TitleViewSet)

review_router = routers.NestedSimpleRouter(title_router, 'titles',
                                           lookup='title')
review_router.register('reviews', ReviewViewSet, basename='title-reviews')

comment_router = routers.NestedSimpleRouter(review_router, 'reviews',
                                            lookup='review')
comment_router.register('comments', CommentViewSet, basename='review-comments')

user_router = routers.SimpleRouter()
user_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('users/me/', UserSelfProfileView.as_view()),
    path('categories/', CategoryListCreateDestroyViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('categories/<slug:slug>/',
         CategoryListCreateDestroyViewSet.as_view({'delete': 'destroy'})),
    path('genres/', GenreListCreateDestroyViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('genres/<slug:slug>/',
         GenreListCreateDestroyViewSet.as_view({'delete': 'destroy'})),
    path('', include(title_router.urls)),
    path('', include(review_router.urls)),
    path('', include(comment_router.urls)),
    path('', include(user_router.urls)),
]
