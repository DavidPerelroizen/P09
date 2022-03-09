from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.


@login_required
def home_page(request):
    return render(request, 'feedapp/home_page.html')


@login_required
def ticket_creation(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket_form.user = request.user
            ticket_form.save(commit=False)
            return redirect('home_page')
    return render(request, 'feedapp/create_ticket.html', context={'ticket_form': ticket_form})
