from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    content = models.TextField()
    content_file = models.FileField(upload_to='projects/', null=True, blank=True)

    def __str__(self):
        return self.name