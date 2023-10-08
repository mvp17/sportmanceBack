from rest_framework import serializers
from .models import DevicesKeyWords


class DevicesKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicesKeyWords
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
