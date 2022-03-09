from django import forms
from . import models


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        if user_id is not None:
            self.fields['user'].queryset = models.Ticket.objects.filter(user=user_id)
        else:
            self.fields['user'].queryset = models.Ticket.objects.none()

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'user', 'image']


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body', 'user']
