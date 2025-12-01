from django.db import models


class Author(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self) -> str: 
		return self.name



class Book(models.Model):

	title = models.CharField(max_length=300)
	publication_year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

	def __str__(self) -> str:
		return f"{self.title} ({self.publication_year})"

