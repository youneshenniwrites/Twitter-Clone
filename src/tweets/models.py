import re

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from .validators import validate_content
from hashtags.signals import parsed_hashtags


class TweetManager(models.Manager):
    '''
    Makes sur that mutiple retweets always
    point to the original parent tweet
    '''

    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        # preventing mutiple retweets; and one retweet in a day
        qs = self.get_queryset().filter(
                user=user, parent=og_parent
                ).filter(
                    timestamp__year=timezone.now().year,
                    timestamp__month=timezone.now().month,
                    timestamp__day=timezone.now().day,
                )
        if qs.exists():
            return None

        obj = self.model(
                parent = og_parent,
                user = user,
                content = parent_obj.content,
            )
        obj.save()
        return obj


class Tweet(models.Model):
    # the self assures that a retweet always points to its parent
    parent      = models.ForeignKey('self', blank=True, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    content     = models.CharField(max_length=255, validators=[validate_content])
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects     = TweetManager()

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('tweets:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-timestamp']


def tweet_save_receiver(sender, instance, created, *args, **kwargs):
    '''
    using Django signals to send notifications to the user
    such as updating the hashtags list in the db when they
    are created and even before they are user -clicked-
    '''

    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)

        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)  

post_save.connect(tweet_save_receiver, sender=Tweet)
