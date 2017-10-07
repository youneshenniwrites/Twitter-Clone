from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models.signals import post_save


class UserProfileManager(models.Manager):
    '''
    remove myself from the list of users following me
    '''
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        # we generate a tuple (user_obj, true)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    # user.profile --> me
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                        related_name='profile')
    # user.profile.following --> users i follow
    # user.followed_by --> users that follow me
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        blank=True,
                                        related_name='followed_by')

    objects = UserProfileManager()  # UserProfile.objects.all()

    def get_following(self):
        '''
        user cannot follow himself
        '''
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def get_follow_url(self):
        '''
        similar to get_absolute_url
        we define a url to direct to after toggle follow
        '''
        return reverse_lazy('profiles:follow', kwargs={'username':self.user.username})

    def get_absolute_url(self):
        return reverse_lazy('profiles:detail', kwargs={'username':self.user.username})

    def __str__(self):
        return str(self.following.all().count())


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    '''
    Django signal to automatically create
    a user profiles when a user object is created
    '''
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
