from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from .models import Tweet

User = get_user_model()


class TweetModelTestCase(TestCase):
    def setUp(self):
        some_random_user = User.objects.create(username='SlowHand')

    def test_tweet_item(self):
        obj = Tweet.objects.create(
                user = User.objects.first(),
                content = 'Here we go!'
                )
        self.assertTrue(obj.content == 'Here we go!')
        self.assertTrue(obj.id == 1)
        absolute_url = reverse('tweets:detail', kwargs={'pk': 1})
        self.assertEqual(obj.get_absolute_url(), absolute_url)

    def test_tweet_url(self):
        obj = Tweet.objects.create(
                user = User.objects.first(),
                content = 'Here we go!'
                )
        absolute_url = reverse('tweets:detail', kwargs={'pk': obj.pk})
        self.assertEqual(obj.get_absolute_url(), absolute_url)
