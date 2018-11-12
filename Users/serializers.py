from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	"""
	image = serializers.SerializerMethodField()
	def get_image(self, obj):
		return settings.MEDIA_URL+obj.image
	"""
	class Meta:
		model = User
		fields = ('username','email','id')
