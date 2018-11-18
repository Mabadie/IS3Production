from django.db import models
from bookrequest.models import BookRequest
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
	
	id= models.AutoField(primary_key=True)
	to=  models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True )
	request= models.ForeignKey(BookRequest,on_delete=models.CASCADE,null=True, blank=True)
	type = models.CharField(max_length=100, blank=True)
	title= models.CharField(max_length=100, blank=True)
	body = models.CharField(max_length=100, blank=True)
	link = models.CharField(max_length=100, blank=True)        
	done =models.BooleanField(default=False);

	def done(self):
                self.done=True
                self.save()


	def build(self,to,request,type,title,body,link):
		self.to = to
		self.request = request
		self.type = type
		self.title = title
		self.body = body
		self.link = link
		
	def send(to,request,type,title,body,link):
		n=Notification();
		n.build(to,request,type,title,body,link)
		n.save();

	class Meta:
		ordering = ('-id',)
		



