import uuid
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    bookName = models.CharField(max_length=100)
    bookAuthor = models.CharField(max_length=100)
    bookDescription = models.TextField(blank=True)

class BookInstance(models.Model):
    # instance types
    PHYSICAL_COPY = 'PB'
    EBOOK = 'EB'
    AUDIOBOOK = 'AB'
    INSTANCE_TYPE_CHOICES = [
        (PHYSICAL_COPY, 'Physical copy'),
        (EBOOK, 'Ebook'),
        (AUDIOBOOK, 'Audiobook'),
    ]

    instanceSerialNum = models.UUIDField(primary_key=True, default=uuid.uuid4)
    instanceBook = models.ForeignKey('Book', on_delete=models.CASCADE)
    instanceType = models.CharField(max_length=20, choices=INSTANCE_TYPE_CHOICES, default=PHYSICAL_COPY)
    borrowedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='borrowedBook', default=None,null=True)

