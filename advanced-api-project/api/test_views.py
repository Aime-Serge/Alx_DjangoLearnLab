from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authenticated tests
        cls.user = User.objects.create_user(username="tester", password="pass1234")

        # Create authors and books
        cls.author1 = Author.objects.create(name="Author One")
        cls.author2 = Author.objects.create(name="Author Two")

        cls.book1 = Book.objects.create(title="Alpha", publication_year=2000, author=cls.author1)
        cls.book2 = Book.objects.create(title="Beta", publication_year=2010, author=cls.author1)
        cls.book3 = Book.objects.create(title="Gamma", publication_year=2020, author=cls.author2)

    def test_list_books_public_access(self):
        url = "/api/books/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return at least the three created books
        self.assertGreaterEqual(len(response.data), 3)

    def test_detail_book_public_access(self):
        url = f"/api/books/{self.book1.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_requires_auth(self):
        url = "/api/books/create/"
        data = {"title": "Delta", "publication_year": 2021, "author": self.author1.pk}
        response = self.client.post(url, data, format="json")
        # Depending on auth backends, DRF may return 401 or 403 for unauthenticated
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        url = "/api/books/create/"
        data = {"title": "Delta", "publication_year": 2021, "author": self.author1.pk}
        # Use session login to authenticate the test client
        self.client.login(username="tester", password="pass1234")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title="Delta").count(), 1)

    def test_update_book_with_pk_authenticated(self):
        url = f"/api/books/{self.book2.pk}/update/"
        data = {"title": "Beta Updated"}
        # Use session login to authenticate the test client
        self.client.login(username="tester", password="pass1234")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Beta Updated")

    def test_delete_book_with_pk_authenticated(self):
        # create a temporary book to delete
        b = Book.objects.create(title="ToDelete", publication_year=1999, author=self.author1)
        url = f"/api/books/{b.pk}/delete/"
        # Use session login to authenticate the test client
        self.client.login(username="tester", password="pass1234")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=b.pk).exists())

    def test_update_no_pk_endpoint(self):
        url = "/api/books/update"
        data = {"id": self.book1.pk, "title": "Alpha Updated"}
        # Use session login to authenticate the test client
        self.client.login(username="tester", password="pass1234")
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha Updated")

    def test_delete_no_pk_endpoint(self):
        b = Book.objects.create(title="ToDelete2", publication_year=2001, author=self.author2)
        url = "/api/books/delete"
        data = {"id": b.pk}
        # Use session login to authenticate the test client
        self.client.login(username="tester", password="pass1234")
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=b.pk).exists())

    def test_filter_by_publication_year(self):
        url = "/api/books/?publication_year=2010"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only book2 should match
        titles = [item["title"] for item in response.data]
        self.assertIn("Beta", titles)

    def test_search_by_title(self):
        url = "/api/books/?search=Gamma"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Gamma", titles)

    def test_ordering_by_publication_year(self):
        url = "/api/books/?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item["publication_year"] for item in response.data]
        # Should be in descending order
        self.assertEqual(years, sorted(years, reverse=True))
