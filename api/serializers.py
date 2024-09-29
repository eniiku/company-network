from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(
    max_length=200,
    help_text="The name of the company"
    )   
    industry = serializers.CharField(
        max_length=100,
        required=False,
        help_text="The industry sector of the company"
    )
    founded_year = serializers.CharField(
        max_length=4,
        required=False,
        help_text="The year the company was founded"
    )

    class Meta:
        swagger_schema_fields = {
            "description": "Represents a company in the network"
        }

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'industry': instance.industry,
            'founded_year': instance.founded_year,
        }

    def create(self, validated_data):
        return Company(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance