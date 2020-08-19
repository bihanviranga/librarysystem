from django.db import models

class Book(models.Model):
    bookName = models.CharField(max_length=100)
    bookAuthor = models.CharField(max_length=100)

