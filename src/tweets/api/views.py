from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsSetPagination


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = 'Not allowed'
        if request.user.is_authenticated():
            is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
            return Response({'liked': is_liked})
        return Response({'message': message}, status=400)


class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = 'Not allowed'
        if tweet_qs.exists() and tweet_qs.count() == 1:
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
            if new_tweet is not None:
                data = TweetModelSerializer(new_tweet).data
                return Response(data)
            message = 'Cannot retweet the same day'
        return Response({'message': message}, status=400)


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
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self):
        '''
        building an api search function
        to integrate with our ajax call
        '''

        requested_user = self.kwargs.get('username')

        if requested_user:
            # if a specific user then show only her tweets
            qs = Tweet.objects.filter(user__username=requested_user).order_by('-timestamp')
        else:
            # show her tweets and her followers
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
