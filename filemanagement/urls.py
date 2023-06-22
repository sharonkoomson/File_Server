from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'filemanagement'

urlpatterns = [
    path('feed/', login_required(views.feed), name='feed'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('send_email/<int:file_id>/', views.send_via_email, name='send_via_email'),
]
