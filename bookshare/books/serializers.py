from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
	
	class Meta:
        	model = Book
	        fields = ('id','owner','title', 'author', 'year','image','aviable')


class BookPostSerializer(serializers.ModelSerializer):

        class Meta:
                model = Book
                fields = ('owner','title', 'author', 'year')
