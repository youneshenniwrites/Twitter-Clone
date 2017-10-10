from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    return render(request, "home.html", {})


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        qs = None
        if query:
            qs = User.objects.filter(
            username__icontains=query
            )
        context = {'users': qs}
        return render(request, 'search.html', context)
