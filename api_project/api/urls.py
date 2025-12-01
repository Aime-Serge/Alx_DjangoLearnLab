from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .views import BookList
from .views import BookViewSet


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request, *args, **kwargs):
    return obtain_auth_token(request, *args, **kwargs)

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path("books/", BookList.as_view(), name="book-list"),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_token, name='api_token_auth'),
]
