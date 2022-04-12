from django.shortcuts import render, redirect
from . import forms
from django.conf import settings
from django.contrib.auth import login


# Create your views here.


def register_page(request):
    """
    This view will enable a user to create his profile on the app.
    :param request: username and valid password
    :return:
    """
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/register_page.html', context={'form': form})
