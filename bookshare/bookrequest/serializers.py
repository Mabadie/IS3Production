from rest_framework import serializers
from books.models import Book
from bookrequest.models import BookRequest

class BookRequestSerializer(serializers.ModelSerializer):
	
	#book= serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only=True)

	class Meta:
		model = BookRequest
		fields = ('id','book','timestamp')



class BookRequestPostSerializer(serializers.ModelSerializer):

        class Meta:
                model = BookRequest
                fields = ('book','user')



class BookRequestPutSerializer(serializers.ModelSerializer):

        class Meta:
                model = BookRequest
                fields = ('id',)
