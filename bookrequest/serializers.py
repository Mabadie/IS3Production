from rest_framework import serializers
from books.models import Book
from bookrequest.models import BookRequest
from books.serializers import BookSerializer

class BookRequestSerializer(serializers.ModelSerializer):
	book = BookSerializer(read_only=True)
	
	class Meta:
		model = BookRequest
		fields = ('id','user','book','state','timestamp')

"""
class BookRequestGetSerializer(serializers.ModelSerializer):

	class Meta:
		model = BookRequest
		fields = ('user','book','state','timestamp')

"""

class BookRequestPostSerializer(serializers.ModelSerializer):

        class Meta:
                model = BookRequest
                fields = ('book','user')



class BookRequestPutSerializer(serializers.ModelSerializer):

        class Meta:
                model = BookRequest
                fields = ('id','calif_owner','calif_reader')
