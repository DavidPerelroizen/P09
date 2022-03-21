from django import forms
from . import models
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

