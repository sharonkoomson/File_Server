from django.shortcuts import render, redirect
from .models import File
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .forms import FileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import os
from .forms import EmailForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Search files'}))
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            'query',
            Submit('submit', 'Search', css_class='btn-primary')
        )


def feed(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        files = File.objects.filter(title__icontains=query).order_by('-uploaded_at')
    else:
        files = File.objects.all().order_by('-uploaded_at')
    
    context = {
        'files': files,
        'form': form,
    }
    return render(request, 'filemanagement/feed.html', context)


def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.downloads += 1  # Increment the download count
    file.save()

    # Get the file's extension
    file_extension = os.path.splitext(file.file.name)[1]

    # Return the file as a download response
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.title}{file_extension}"'
    return response


def send_via_email(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            subject = 'File Download'
            message = render_to_string('filemanagement/email_message.html', {'file': file})

            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_message.content_subtype = 'html'  # Set the content type to HTML

            # Attach the file
            email_message.attach_file(file.file.path)
            email_message.send()

            file.emails_sent += 1
            file.save()

            return redirect('filemanagement:feed')
    else:
        form = EmailForm()

    context = {
        'file': file,
        'form': form,
    }
    return render(request, 'filemanagement/send_email.html', context)



