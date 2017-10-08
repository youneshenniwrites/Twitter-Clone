from django.shortcuts import render
from django.views import View

from .models import HashTag


class HashTagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = HashTag.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tweet_hashtag.html', {"obj": obj})
