from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework import routers

from .views import PostViewSet, CommentViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('posts/(?P<post_id>.d+)/comments', CommentViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
