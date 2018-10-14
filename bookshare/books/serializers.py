from rest_framework import serializers
from django.conf import settings
from books.models import Book

class BookSerializer(serializers.ModelSerializer):

	image = serializers.SerializerMethodField()
	def get_image(self, obj):
		return settings.MEDIA_URL+obj.image

	class Meta:
		model = Book
		fields = ('id','owner','title', 'author', 'year','image','aviable')


class BookPostSerializer(serializers.ModelSerializer):

        class Meta:
                model = Book
                fields = ('owner','title', 'author', 'year')
