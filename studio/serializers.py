from rest_framework import serializers

from .models import Design, Master


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ["id", "name", "specialization"]


class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = ["id", "title", "style", "price", "image_url", "master"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ціна має бути більшою за 0.")
        return value
