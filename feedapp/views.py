from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value, Q
import requests

# Create your views here.


@login_required
def home_page(request):
    follower = models.UserFollows.objects.filter(user=request.user).values('followed_user')
    tickets = models.Ticket.objects.filter(Q(user=request.user) | Q(user__in=follower))
    reviews = models.Review.objects.filter(Q(user=request.user) | Q(user__in=follower))
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
    form_ticket = forms.TicketForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        form_ticket = forms.TicketForm(request.POST)
        if form.is_valid() and form_ticket.is_valid():
            ticket_form = form_ticket.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            ticket_to_answer = models.Ticket.objects.last()
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.ticket = ticket_to_answer
            review_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/create_review.html', context={'review_form': form, 'ticket_form': form_ticket})


@login_required
def answer_to_ticket(request, ticket_id):
    ticket_to_answer = get_object_or_404(models.Ticket, id=ticket_id)
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        if form_review.is_valid():
            review_form = form_review.save(commit=False)
            review_form.user = request.user
            review_form.ticket = ticket_to_answer
            review_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/answer_ticket.html', context={'review_form': form_review,
                                                                  'ticket': ticket_to_answer})


@login_required
def follow_user(request):
    followed_users = models.UserFollows.objects.filter(user=request.user)
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    form = forms.FollowUserForm()
    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            follow_user_form = form.save(commit=False)
            follow_user_form.user = request.user
            follow_user_form.save()
            return redirect('subscription_page')
    return render(request, 'feedapp/subscription_page.html', context={'subscription_form': form,
                                                                      'followed_users': followed_users,
                                                                      'followers': followers})


@login_required
def unfollow_user(request, user_id):
    users_to_unfollow = models.UserFollows.objects.filter(user=request.user, followed_user=user_id)
    form = forms.DeletePostForm()
    if request.method == 'POST':
        if 'delete_post' in request.POST:
            form = forms.DeletePostForm(request.POST)
            if form.is_valid():
                users_to_unfollow.delete()
                return redirect('subscription_page')
    return render(request, 'feedapp/unsubscription_page.html', context={'deletion_form': form,
                                                                        'users_to_unfollow':
                                                                            users_to_unfollow})




@login_required
def my_posts_page(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'feedapp/my_posts_page.html', context={'posts': posts})


@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            ticket_form = form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            ticket.delete()
            return redirect('home_page')
    return render(request, 'feedapp/ticket_update.html', context={'ticket_update': form})


@login_required
def modify_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.save()
            review.delete()
            return redirect('home_page')
    return render(request, 'feedapp/review_update.html', context={'review_update': form})


@login_required
def delete_ticket(request, ticket_id):
    post_to_delete = get_object_or_404(models.Ticket, id=ticket_id)
    delete_post_form = forms.DeletePostForm()
    if request.method == 'POST':
        if 'delete_post' in request.POST:
            delete_post_form = forms.DeletePostForm(request.POST)
            if delete_post_form.is_valid():
                post_to_delete.delete()
                return redirect('my_posts_page')
    return render(request, 'feedapp/delete_ticket_page.html', context={'delete_post_form': delete_post_form,
                                                                       'post_to_delete': post_to_delete})


@login_required
def delete_review(request, review_id):
    post_to_delete = get_object_or_404(models.Review, id=review_id)
    delete_post_form = forms.DeletePostForm()
    if request.method == 'POST':
        if 'delete_post' in request.POST:
            delete_post_form = forms.DeletePostForm(request.POST)
            if delete_post_form.is_valid():
                post_to_delete.delete()
                return redirect('my_posts_page')
    return render(request, 'feedapp/delete_review_page.html', context={'delete_post_form': delete_post_form,
                                                                       'post_to_delete': post_to_delete})
