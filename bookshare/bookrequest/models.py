from django.db import models
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
		(2,'Entregado'),
		(3,'Devuelto/Finalizada'),
		(4,'Rechazada/Finalizada'),
	)

	user= models.ForeignKey(User,on_delete=models.CASCADE)
	book= models.ForeignKey(Book,on_delete=models.CASCADE)
	state= models.IntegerField(choices=REQUEST_STATES,default=0)
	timestamp = models.DateTimeField(default=datetime.date.today)
	

	def accept(self):
		book=Book.objects.get(id=self.book.id)
		book.share()
		self.state=1
		self.save()	

	class Meta:
		unique_together = (("user", "book"),)
		ordering=('timestamp',)


	
	
