from rest_framework import serializers
from .models import DataInput


class DataInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataInput
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
