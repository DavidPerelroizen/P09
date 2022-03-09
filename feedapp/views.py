from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms, models

# Create your views here.


@login_required
def home_page(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'feedapp/home_page.html', context={'tickets': tickets})


@login_required
def ticket_creation(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.user = request.user
            ticket_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/create_ticket.html', context={'ticket_form': ticket_form})
