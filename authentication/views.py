from django.shortcuts import render
from . import forms
from django.contrib.auth import login, authenticate


# Create your views here.

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Welcome {user.username}! You are connected.'
            else:
                message = 'Wrong identifiers.'
    return render(
        request, 'authentication/login_page.html', context={'form': form, 'message': message})
