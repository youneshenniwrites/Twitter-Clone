from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse_lazy('profiles:detail', kwargs={'username': obj.username})

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'url',
        ]
