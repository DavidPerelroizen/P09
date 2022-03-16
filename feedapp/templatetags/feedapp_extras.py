from django import template
from feedapp import models
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.filter
def ticket_has_review(value):
    test_existing_reviews = False
    review = models.Review.objects.filter(ticket=value)
    if review:
        test_existing_reviews = True
    return test_existing_reviews


@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Published {int(seconds_ago // MINUTE)} minutes ago.'
    elif seconds_ago <= DAY:
        return f'Published {int(seconds_ago // HOUR)} hours ago.'
    return f'Published on {posted_at.strftime("%d %b %y à %Hh%M")}'


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'You'
    return user.username
