# Generated by Django 4.2.2 on 2023-06-21 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filemanagement', '0002_file_downloads_file_emails_sent_file_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_url',
        ),
    ]
