''' Building a CRUD application with the following views '''

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView

from .models import Tweet
from .forms import TweetModelForm


class TweetCreateView(CreateView):
    form = TweetModelForm


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()


class TweetListView(ListView):
    queryset = Tweet.objects.all()
