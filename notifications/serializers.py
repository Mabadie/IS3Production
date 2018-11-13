from rest_framework import serializers
from django.conf import settings
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):

	class Meta:
                model = Notification
                fields = ('id','to','request','type', 'title', 'body','link','timestamp','done')


