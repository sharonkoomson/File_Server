from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('filemanagement:feed')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template = 'registration/password_reset_email.html'
    success_url = '/password-reset/done/'