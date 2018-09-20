from django.db import models
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Book(models.Model):
	id= models.AutoField(primary_key=True)
	owner =  models.ForeignKey(User,on_delete=models.CASCADE)
	title = models.CharField(max_length=100, blank=True, default='')
	author = models.TextField()
	year = models.IntegerField(default=False)
	image= models.CharField(max_length=100, blank=True, default='B64encoded')
	aviable = models.BooleanField(default=True);

	def owned_by(self,user):
		return self.owner.id==user.id

	def share(self):
		self.aviable=False
		self.save()

	class Meta:
		ordering = ('title',)
