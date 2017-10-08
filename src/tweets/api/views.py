from rest_framework import generics, permissions
from django.db.models import Q

from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        a tweet must be posted by a specific user
        '''
        serializer.save(user=self.request.user)


class TweetListAPIView(generics.ListAPIView):
    '''
    displays the list of tweets from the user and her followers
    '''

    serializer_class = TweetModelSerializer
    # permission_classes = pass
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        '''
        building an api search function
        to integrate with our ajax call
        '''

        im_following = self.request.user.profile.get_following()
        qs1 = Tweet.objects.filter(user__in=im_following)
        qs2 = Tweet.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct().order_by('-timestamp')
        query = self.request.GET.get('q' or None)
        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            ).distinct()
        return qs
