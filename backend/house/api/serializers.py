from rest_framework import serializers

from house.models import Apartment, House, WaterMeter, WaterMeterReading


class WaterMeterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterMeterReading
        fields = ['id', 'reading_date', 'value', 'water_meter']


class WaterMeterSerializer(serializers.ModelSerializer):
    readings = WaterMeterReadingSerializer(many=True, read_only=True)

    class Meta:
        model = WaterMeter
        fields = ['id', 'name', 'serial_number', 'apartment', 'readings']


class ApartmentSerializer(serializers.ModelSerializer):
    water_meters = WaterMeterSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ['id', 'number', 'area', 'house', 'water_meters']


class HouseDetailSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['id', 'city', 'street', 'house_number', 'apartments']


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'city', 'street', 'house_number']


class ApartmentHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartment
        fields = (
            'id', 'number', 'area',
        )
