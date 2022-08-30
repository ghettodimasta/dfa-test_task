from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Photo(models.Model):
    img = models.ImageField(upload_to='gallery')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

