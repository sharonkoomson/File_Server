from django.contrib import admin

# Register your models here.
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'downloads', 'emails_sent', 'uploaded_at']
    readonly_fields = ['downloads', 'emails_sent', 'uploaded_at']