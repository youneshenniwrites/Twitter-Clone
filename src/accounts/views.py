from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import DetailView


User = get_user_model()


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()

    def get_object(self):
        '''
        override the get_object method to lookup
        for a username parameter; defaults to pk or slug
        '''
        return get_object_or_404(
                                User,
                                username__iexact=self.kwargs['username']
                                )
