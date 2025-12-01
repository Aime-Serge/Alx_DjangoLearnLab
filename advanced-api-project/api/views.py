from typing import Any

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters as drf_filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

	filterset_fields = ["title", "author", "publication_year"]

	search_fields = ["title", "author__name"]

	ordering_fields = ["title", "publication_year"]
	ordering = ["title"]

	def get_queryset(self):
		return super().get_queryset()


class BookDetailView(generics.RetrieveAPIView):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):


	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer: BookSerializer) -> None:

		serializer.save()


class BookUpdateView(generics.UpdateAPIView):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	def perform_update(self, serializer: BookSerializer) -> None:
		serializer.save()


class BookDeleteView(generics.DestroyAPIView):

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]


class BookUpdateNoPKView(APIView):

	permission_classes = [IsAuthenticated]

	def _get_instance(self, request: Request) -> Book:
		book_id = request.data.get("id") or request.data.get("pk")
		if not book_id:
			raise ValueError("Missing 'id' or 'pk' in request body")
		return get_object_or_404(Book, pk=book_id)

	def put(self, request: Request, *args, **kwargs) -> Response:
		try:
			instance = self._get_instance(request)
		except ValueError as exc:
			return Response({"detail": str(exc)}, status=400)

		serializer = BookSerializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def patch(self, request: Request, *args, **kwargs) -> Response:
		try:
			instance = self._get_instance(request)
		except ValueError as exc:
			return Response({"detail": str(exc)}, status=400)

		serializer = BookSerializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class BookDeleteNoPKView(APIView):

	permission_classes = [IsAuthenticated]

	def delete(self, request: Request, *args, **kwargs) -> Response:
		book_id = request.data.get("id") or request.data.get("pk")
		if not book_id:
			return Response({"detail": "Missing 'id' or 'pk' in request body"}, status=400)

		instance = get_object_or_404(Book, pk=book_id)
		instance.delete()
		return Response(status=204)

