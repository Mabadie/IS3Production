from rest_framework.views import APIView
from rest_framework import permissions
from notifications.models import Notification
from django.db.models import Q
from notifications.serializers import NotificationSerializer
from rest_framework.response import Response
import datetime
import logging
logger = logging.getLogger('herokuLogger')
# Create your views here.

class NotificationsList(APIView):

	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, format=None):
		logger.info("Recibi un pedido de notificaciones {}".format(datetime.datetime.now()))
		notifications = Notification.objects.filter(Q(to=self.request.user.id))
		logger.info("Notificaciones obtenidas de bd {}".format(datetime.datetime.now()))
		serializer = NotificationSerializer(notifications, many=True)
		logger.info("Notificaciones serializadas {}".format(datetime.datetime.now()))
		return Response(serializer.data)

