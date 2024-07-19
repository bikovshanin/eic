from rest_framework import serializers

from house.api.serializers import HouseSerializer
from rent.models import CalculationResult


class CalculationResultSerializer(serializers.ModelSerializer):
    apartment = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, obj):
        return obj.water_cost + obj.maintenance_cost

    def get_apartment(self, obj):
        return {
            'id': obj.apartment.id,
            'number': obj.apartment.number,
        }

    class Meta:
        model = CalculationResult
        fields = (
            'id',
            'month',
            'apartment',
            'water_cost',
            'maintenance_cost',
            'total_cost'
        )


class ResultSerializer(serializers.Serializer):
    house = HouseSerializer()
    apartment = CalculationResultSerializer(many=True)
