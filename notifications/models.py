from django.db import models
from bookrequest.models import BookRequest
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
	id= models.AutoField(primary_key=True)
	to=  models.ForeignKey(User,on_delete=models.CASCADE)
	request= models.ForeignKey(BookRequest,on_delete=models.CASCADE)
	type = models.CharField(max_length=100, blank=True)
	title= models.CharField(max_length=100, blank=True)
	body = models.CharField(max_length=100, blank=True)
	link = models.CharField(max_length=100, blank=True)        
	timestamp = models.DateTimeField(default=datetime.date.today)
	done =models.BooleanField(default=False);

	def send(notif):
		n = Notification.objects.create_notification(notif)
		n.save()

	def done(self):
                self.done=True
                self.save()

	class Meta:
		ordering = ('timestamp',)
