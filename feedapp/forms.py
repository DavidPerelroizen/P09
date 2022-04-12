from django import forms
from . import models


class TicketForm(forms.ModelForm):
    edit_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    edit_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'),
                                                                  (5, '5')])

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']


class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)
