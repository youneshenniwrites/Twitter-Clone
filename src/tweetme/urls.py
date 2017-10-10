from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from .views import home, SearchView
from hashtags.views import HashTagView
from tweets.views import TweetListView
from tweets.api.views import SearchTweetAPIView
from hashtags.api.views import TagTweetAPIView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TweetListView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name='hashtag'),
    url(r'^tweets/', include('tweets.urls', namespace='tweets')),
    url(r'^api/tags/(?P<hashtag>.*)/$', TagTweetAPIView.as_view(), name='tag-tweet-api'),
    url(r'^api/search/$', SearchTweetAPIView.as_view(), name='search-api'),
    url(r'^api/tweets/', include('tweets.api.urls', namespace='tweets-api')),
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
    url(r'^', include('accounts.urls', namespace='profiles')),
]


if settings.DEBUG: # for a production environment
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
