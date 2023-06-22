from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'file']

class EmailForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))