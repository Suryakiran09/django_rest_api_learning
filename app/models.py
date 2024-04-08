from django.db import models

class Books(models.Model):
    book_name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    address = models.CharField(max_length=30)
    quantity = models.IntegerField()

class Genre(models.Model):
    genre_name = models.CharField(max_length=30)
    books = models.ManyToManyField(Books)