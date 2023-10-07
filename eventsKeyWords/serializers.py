from rest_framework import serializers
from .models import EventsKeyWords


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsKeyWords
        fields = '__all__'
