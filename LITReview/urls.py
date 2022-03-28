"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from feedapp.views import home_page, ticket_creation, review_creation, answer_to_ticket, follow_user, my_posts_page, \
    modify_ticket, modify_review, delete_ticket, delete_review, unfollow_user, follow_user_bis
from authentication.views import register_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login_page.html',
        redirect_authenticated_user=True),
         name='login_page'),
    path('logout_page/', LogoutView.as_view(),
         name='logout_page'),
    path('home_page/', home_page, name='home_page'),
    path('register_page/', register_page, name='register_page'),
    path('create_ticket/', ticket_creation, name='create_ticket'),
    path('create_review/', review_creation, name='create_review'),
    path('feedapp/<int:ticket_id>', answer_to_ticket, name='answer_ticket'),
    path('subscription_page/', follow_user, name='subscription_page'),
    path('my_posts_page/', my_posts_page, name='my_posts_page'),
    path('feedapp/<int:ticket_id>/ticket_update', modify_ticket, name='ticket_update'),
    path('feedapp/<int:review_id>/review_update', modify_review, name='review_update'),
    path('feedapp/<int:ticket_id>/delete_ticket_page', delete_ticket, name='delete_ticket_page'),
    path('feedapp/<int:review_id>/delete_review_page', delete_review, name='delete_review_page'),
    path('feedapp/<int:user_id>/unsubscription_page', unfollow_user, name='unsubscription_page'),
    path('feedapp/subscription/<int:user_id>', follow_user_bis, name='subscription'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
