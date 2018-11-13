from rest_framework import serializers
from django.conf import settings
from notifications.models import Notification
from bookrequest.serializers import BookRequestSerializer

class NotificationSerializer(serializers.ModelSerializer):
	
	request = BookRequestSerializer(read_only=True)	

	class Meta:
                model = Notification
                fields = ('id','to','request','type', 'title', 'body','link','done')



