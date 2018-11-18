from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import datetime
from django.contrib.auth.models import User
from books.models import Book

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class BookRequest(models.Model):

	REQUEST_STATES=	(
		(0,'Enviada'),
		(1,'Aceptada'),
		(2,'Entregado-SinConfirmacion'),
		(3,'Entregado-Confirmado'),
		(4,'Devuelto-SinConfirmacion'),
		(5,'Devuelto-Confirmado-Sin-Calificar'),
		(6,'Rechazada/Finalizada'),
		(7,'Devuelto-Calificado-Owner'),
		(8,'Devuelto-Calificado-Reader'),
		(9,'Devuelto')
	)

	user= models.ForeignKey(User,on_delete=models.CASCADE)
	book= models.ForeignKey(Book,on_delete=models.CASCADE)
	state= models.IntegerField(choices=REQUEST_STATES,default=0)
	calif_owner= models.IntegerField(default=0)
	calif_reader= models.IntegerField(default=0)
	timestamp = models.DateTimeField(default=datetime.date.today)
	

	def accept(self):
		#owner=yo && state=0
		self.state=1
		self.save()
		#genera notificacion de aceptacion

	def deliver(self):
		#owner=yo && state=1
		self.state=2
		self.save()
		#genera notificacion entrega
	
	def confirm_delivered(self):
		#user=yo && state=2
		self.state=3
		self.save()
		#genera notificacion confirmacion entrega
		
	def give_back(self):
		#user=yo && state=3
		self.state=4
		self.save()
		#genera notificacion devolucion		

	def confirm_returned(self):
		#owner=yo && state=4
		self.state=5
		self.save()
		#genera notificacion confirmacion devolucion

	def reject(self):
		#owner=yo && state = 0
		self.state=6
		self.save()
		#genera notificacion de rechazo


	def calification_owner(self):
		if(self.state==5):
			self.state=7
		else:
			self.state=9
		self.save()

	def calification_reader(self):
		if(self.state==5):
			self.state=8
		else:
			self.state=9
		self.save()

	class Meta:
		unique_together = (("user", "book"),)
		ordering=('timestamp',)

