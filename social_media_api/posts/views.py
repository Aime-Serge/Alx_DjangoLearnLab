from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author
        if comment.post.author != self.request.user:
            from django.contrib.contenttypes.models import ContentType
            from notifications.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target_content_type=ContentType.objects.get_for_model(Comment),
                target_object_id=comment.id
            )

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create notification
        from django.contrib.contenttypes.models import ContentType
        from notifications.models import Notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )
        
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
