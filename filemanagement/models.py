from django.db import models

# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)