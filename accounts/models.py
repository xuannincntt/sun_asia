from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    tel = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.email