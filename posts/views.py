from rest_framework import viewsets

from .serializers import PostSerializer
from .models import Post
from .permissions import PostPermissions

class PostView(viewsets.ModelViewSet):
  serializer_class = PostSerializer
  model = Post
  queryset = Post.objects.all()
  permission_classes = (PostPermissions,)
