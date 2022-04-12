from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import authentication.models
from . import forms, models
from itertools import chain
from django.db.models import CharField, Value, Q

# Create your views here.


@login_required
def home_page(request):
    """"
    Defines the home_page view and the objects that would be displayed.
    """
    follower = models.UserFollows.objects.filter(user=request.user).values('followed_user')
    tickets = models.Ticket.objects.filter(Q(user=request.user) | Q(user__in=follower))
    reviews = models.Review.objects.filter(Q(user=request.user) | Q(user__in=follower) |
                                           Q(ticket__in=tickets))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)

    # Implements a pagination to have maximum 5 elements per page
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'feedapp/home_page.html', context={'page_obj': page_obj})


@login_required
def ticket_creation(request):
    """
    This view will feed the ticket creation page
    :param request:
    :return:
    """
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
    """
    This view will feed the review creation page
    :param request:
    :return:
    """
    form = forms.ReviewForm()
    form_ticket = forms.TicketForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        form_ticket = forms.TicketForm(request.POST, request.FILES)
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
    """
    This view helps to create a review about a specific ticket
    :param request:
    :param ticket_id:
    :return:
    """
    ticket_to_answer = get_object_or_404(models.Ticket, id=ticket_id)  # Get the ticket to be answered to
    form_review = forms.ReviewForm()  # Initialize a review form
    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        if form_review.is_valid():
            review_form = form_review.save(commit=False)
            review_form.user = request.user  # Put the current user as the creator of the review
            review_form.ticket = ticket_to_answer  # Put the specific ticket in the review attributes
            review_form.save()
            return redirect('home_page')
    return render(request, 'feedapp/answer_ticket.html', context={'review_form': form_review,
                                                                  'ticket': ticket_to_answer})


@login_required
def follow_user(request):
    """
    This function operates queries that will display the users a user can follow, the users it already follows, and
    the list of its followers.
    :param request:
    :return:
    """
    followed_users = models.UserFollows.objects.filter(user=request.user)
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    users_to_follow = authentication.models.User.objects.exclude(Q(id=request.user.id) |
                                                                 Q(id__in=followed_users.values('followed_user')))
    return render(request, 'feedapp/subscription_page.html', context={'followed_users': followed_users,
                                                                      'followers': followers,
                                                                      'users_to_follow': users_to_follow})


@login_required
def follow_user_bis(request, user_id):
    """
    This function associates a user with its follower (request.user)
    :param request:
    :param user_id:
    :return:
    """
    try:
        user = authentication.models.User.objects.get(id=user_id)
    except Exception:
        pass
    user_follows = models.UserFollows()
    user_follows.user = request.user
    user_follows.followed_user = user
    user_follows.save()
    return redirect('subscription_page')


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
    """
    This function will operate queries that will extract and gather all the tickets and reviews created by the user
    himself
    :param request:
    :return:
    """
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)

    # Implements a pagination to have maximum 5 elements per page
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'feedapp/my_posts_page.html', context={'page_obj': page_obj})


@login_required
def modify_ticket(request, ticket_id):
    """
    This function will help to modify a specific ticket based on its ID
    :param request:
    :param ticket_id:
    :return:
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket_form = form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
            ticket.delete()
            return redirect('home_page')
    return render(request, 'feedapp/ticket_update.html', context={'ticket_update': form})


@login_required
def modify_review(request, review_id):
    """
    This function will help to modify a specific review based on its ID
    :param request:
    :param review_id:
    :return:
    """
    review = get_object_or_404(models.Review, id=review_id)
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review_form = form.save(commit=False)
            review_form.user = request.user
            review_form.ticket = review.ticket
            review_form.save()
            review.delete()
            return redirect('home_page')
    return render(request, 'feedapp/review_update.html', context={'review_update': form, 'ticket': review.ticket})


@login_required
def delete_ticket(request, ticket_id):
    """
    Ticket deletion specific view
    :param request:
    :param ticket_id:
    :return:
    """
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
    """
    Review deletion specific view
    :param request:
    :param review_id:
    :return:
    """
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
