# Generated by Django 4.0.3 on 2022-03-23 20:54

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('feedapp', '0002_alter_review_rating_alter_review_ticket'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollows',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('followed_user')), _negated=True), name='no_self_follow'),
        ),
    ]