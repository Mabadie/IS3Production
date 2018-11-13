from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from notifications.models import Notification
from django.db.models import Q
from notifications.serializers import NotificationSerializer
from rest_framework.response import Response

# Create your views here.

class NotificationsList(APIView):

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, format=None):
		notifications = Notification.objects.filter(Q(to=self.request.user.id))
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

