from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
	
	class Meta:
        	model = Book
	        fields = ('id','owner','title', 'author', 'year','aviable')


class BookPostSerializer(serializers.ModelSerializer):

        class Meta:
                model = Book
                fields = ('owner','title', 'author', 'year')
