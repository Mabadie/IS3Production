from django.db import models

# Create your models here.

class Notification(models.Model):
        id= models.AutoField(primary_key=True)
        request= models.ForeignKey(BookRequest,on_delete=models.CASCADE)

        class Meta:
                ordering = ('timestamp',)

