from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse

class Book(models.Model):
    # Basic book information
    title = models.CharField(max_length=200, db_index=True, help_text="Enter the book title")
    author = models.CharField(max_length=100, db_index=True, help_text="Enter the author's name")
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(timezone.now().year)
        ],
        help_text="Enter the year the book was published"
    )
    
    # Additional book details
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 Character ISBN number',
        null=True,
        blank=True
    )
    
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NON', 'Non-Fiction'),
        ('SCI', 'Science'),
        ('TEH', 'Technology'),
        ('HIS', 'History'),
        ('BIO', 'Biography'),
        ('OTH', 'Other'),
    ]
    
    genre = models.CharField(
        max_length=3,
        choices=GENRE_CHOICES,
        default='OTH',
        help_text='Select the book genre'
    )
    
    description = models.TextField(
        max_length=1000,
        help_text='Enter a brief description of the book',
        null=True,
        blank=True
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Enter the book price'
    )
    
    # Book status
    AVAILABILITY_STATUS = [
        ('AV', 'Available'),
        ('ON', 'On Loan'),
        ('RS', 'Reserved'),
        ('NA', 'Not Available'),
    ]
    
    status = models.CharField(
        max_length=2,
        choices=AVAILABILITY_STATUS,
        default='AV',
        help_text='Book availability'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publication_year', 'title']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['isbn']),
            models.Index(fields=['status']),
        ]
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
    
    def get_absolute_url(self):
        """Returns the URL to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])
    
    @property
    def is_available(self):
        """Check if the book is available for loan."""
        return self.status == 'AV'
