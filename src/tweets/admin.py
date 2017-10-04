from django.contrib import admin

from .models import Tweet
from .forms import TweetModelForm


class TweetModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetModelAdmin)
