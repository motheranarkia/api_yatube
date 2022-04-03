from rest_framework import viewsets, permissions
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group, Comment


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пермишн для проверки, является ли юзер автором поста"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки CRUD для posts"""
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки CRUD для groups"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки CRUD для comments"""
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def perform_update(self, serializer):
    if serializer.instance.author != self.request.user:
        raise PermissionDenied('Изменение чужого контента запрещено!')
    super(PostViewSet, self).perform_update(serializer)
