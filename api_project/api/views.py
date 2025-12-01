from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            permission_classes = [permissions.IsAdminUser]
        elif self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]