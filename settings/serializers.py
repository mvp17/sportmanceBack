from rest_framework import serializers
from .models import SessionParameters


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionParameters
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
