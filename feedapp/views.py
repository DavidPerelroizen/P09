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
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket_form = form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/create_ticket.html', context={'ticket_form': form})


@login_required
def review_creation(request):
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/create_review.html', context={'review_form': form})
