from rest_framework import serializers
from .models import DataFile


class DevicesKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = '__all__'
