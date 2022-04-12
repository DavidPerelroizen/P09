from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from LITReview import settings
from PIL import Image

# Create your models here.


class Ticket(models.Model):
    """
    This model defines the structure of a ticket and the constraints associated to each ticket parameters.
    """
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (100, 100)

    def resize_image(self):
        """
        This function helps to resize an image uploaded by the user in order to avoid overloading the server
        :return: same image but resized using the IMAGE_MAX_SIZE variable
        """
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        We redefine the save function in order to include the image resizing in it.
        :param args:
        :param kwargs:
        :return:
        """
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """
    This model defines the structure of a review and the constraints associated to each review parameters.
    """
    ticket = models.ForeignKey(to=Ticket, null=True, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """
    This model defines the relationship between a user and the other user that he follows.
    """
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        # Makes sure that there is a unique tuple between a user and a follower
        unique_together = ('user', 'followed_user')
        # Makes sure that a user can't follow himself
        constraints = [models.CheckConstraint(check=~models.Q(user=models.F('followed_user')), name='no_self_follow')]
