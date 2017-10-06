''' Building a CRUD application with the following views '''

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
                CreateView,
                DetailView,
                DeleteView,
                ListView,
                UpdateView
                )


from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/tweet_create.html'


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/tweet_update.html'


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/tweet_delete.html'
    success_url = reverse_lazy("tweets:list")


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()


class TweetListView(ListView):
    def get_queryset(self):
        '''
        building a search function
        '''

        qs = Tweet.objects.all()
        query = self.request.GET.get('q' or None)
        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            ).distinct()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweets:create")
        return context
