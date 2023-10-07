from rest_framework import serializers
from .models import SessionParameters


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionParameters
        fields = '__all__'
