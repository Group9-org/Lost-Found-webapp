from django.db import models
from django.contrib.auth.models import User

from django.db import models

class LostItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Documents', 'Documents'),
        ('Accessories', 'Accessories'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Other'
    )
    contact = models.CharField(max_length=100, null=True, blank=True)
    

    image = models.ImageField(
        upload_to='lost_items/',
        null=True,
        blank=True
    )

    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FoundItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
