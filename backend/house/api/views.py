from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from house.api.serializers import (ApartmentSerializer, HouseDetailSerializer,
                                   HouseSerializer,)
from house.models import Apartment, House, WaterMeter, WaterMeterReading


class HouseViewSet(viewsets.ViewSet):

    def list(self, request):
        houses = House.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        house = get_object_or_404(House, id=pk)
        serializer = HouseDetailSerializer(house)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApartmentListView(generics.ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class ApartmentDetailView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        street = request.query_params.get('street')
        house_number = request.query_params.get('house_number')
        apartment_number = request.query_params.get('apartment_number')

        if not city or not street or not house_number or not apartment_number:
            return Response(
                {
                    'error': 'City, street, house number, '
                             'and apartment number are required.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            house = House.objects.get(
                city=city, street=street,
                house_number=house_number
            )
            apartment = Apartment.objects.get(
                house=house,
                number=apartment_number
            )
        except House.DoesNotExist:
            return Response(
                {'error': 'House not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Apartment.DoesNotExist:
            return Response(
                {'error': 'Apartment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ApartmentSerializer(apartment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        readings = request.data.get('readings')

        if not readings:
            return Response(
                {'error': 'Readings are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        for reading_data in readings:
            meter_id = reading_data.get('meter_id')
            value = reading_data.get('value')

            if not meter_id or value is None:
                return Response(
                    {'error': 'Meter ID, and value '
                              'are required for each reading.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                value = float(value)
                if value < 0:
                    raise ValueError('Value cannot be negative.')
            except ValueError:
                return Response({
                    'error': 'Value must be a non-negative number.'
                }, status=status.HTTP_400_BAD_REQUEST)

            meter = get_object_or_404(WaterMeter, id=meter_id)
            latest_reading = WaterMeterReading.objects.filter(
                water_meter=meter
            ).order_by('-reading_date').first()

            if latest_reading and value < latest_reading.value:
                return Response(
                    {
                        'error': 'Value cannot be less '
                                 'than the previous reading.'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            WaterMeterReading.objects.create(water_meter=meter,
                                             value=value)

        return Response(
            {'message': 'Readings recorded successfully.'},
            status=status.HTTP_201_CREATED
        )
