from django.db import models

# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='A generic file')
    file = models.FileField(upload_to='files/', default=None)
    downloads = models.PositiveIntegerField(default=0)
    emails_sent = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return self.file.url[len('files/'):]  # Remove 'files/' segment from the URL


    def __str__(self):
        return self.title