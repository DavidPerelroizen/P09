from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value

# Create your views here.


@login_required
def home_page(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feedapp/home_page.html', context={'posts': posts})


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
