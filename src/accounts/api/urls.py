from django.conf.urls import url

from django.views.generic.base import RedirectView

from tweets.api.views import TweetListAPIView


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/tweets/$', TweetListAPIView.as_view(), name='list'),
]
