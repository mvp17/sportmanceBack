from rest_framework import serializers
from .models import EventsKeyWords


class EventsKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsKeyWords
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
