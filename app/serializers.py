from rest_framework import serializers
from app.models import *

from rest_framework import serializers
from app.models import Books, Genre

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)  # Here, we specify the related serializer for the books field
    class Meta:
        model = Genre
        fields = "__all__"
    
    def create(self, validated_data):
        books = validated_data.pop('books')
        genre = Genre.objects.get_or_create(**validated_data)[0]

        if isinstance(books, list):
            for book in books:
                book_instance = Books.objects.create(**book)
                genre.books.add(book_instance)
        else:
            book_instance = Books.objects.create(**books)
            genre.books.add(book_instance)

        genre.save()
        return genre
    
    def update(self, instance, validated_data):
        instance.genre_name = validated_data.get('genre_name', instance.genre_name)
        books_data = validated_data.pop('books', [])

        for book in instance.books.all():
            book.delete()

        for book_data in books_data:
            books = Books.objects.create(**book_data)
            instance.books.add(books)

        instance.save()
        return instance
    
    
# class book_serializer(serializers.ModelSerializer):
#     custom_method = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = Books
#         fields = "__all__"
    
#     def get_custom_method(self, obj):
#         return "hi"


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=30)