from rest_framework import generics, permissions
from django.db.models import Q

from tweets.models import Tweet
from .serializers import TweetModelSerializer


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        a tweet must be posted by a specific user
        '''
        serializer.save(user=self.request.user)


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    # permission_classes = pass

    def get_queryset(self):
        '''
        building an api search function
        to integrate with our ajax call
        '''

        qs = Tweet.objects.all()
        query = self.request.GET.get('q' or None)
        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            ).distinct()
        return qs
