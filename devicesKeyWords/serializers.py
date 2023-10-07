from rest_framework import serializers
from .models import DevicesKeyWords


class DevicesKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicesKeyWords
        fields = '__all__'
