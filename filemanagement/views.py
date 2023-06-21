from django.shortcuts import render, redirect
from .models import File
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .forms import FileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import os

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


def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            return redirect('file_detail', file_id=file.id)
    else:
        form = FileForm()
    return render(request, 'admin/upload_file.html', {'form': form})


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