from datetime import date, datetime

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.tasks import calculate_bills_for_house
from house.models import House
from rent.api.serializers import ResultSerializer
from rent.models import CalculationResult


class CalculationView(APIView):

    def month_validation(self, month_str):

        try:
            month = datetime.strptime(month_str, '%Y-%m-%d').date()
        except ValueError:
            return None, Response(
                {'error': 'Invalid date format, should be YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if month > date.today():
            return None, Response(
                {'error': 'Date cannot be in the future'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return month, None

    def get_month_from_request(self, request):
        month_str = (
            request.data.get('date')
            if request.method == 'POST'
            else request.query_params.get('date')
        )
        if not month_str:
            return None, Response(
                {'error': 'Date is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.month_validation(month_str)

    def post(self, request, house_id):
        month, error_response = self.get_month_from_request(request)
        if error_response:
            return error_response

        calculate_bills_for_house.delay(house_id, month)
        return Response({'result': 'success'})

    def get(self, request, house_id):
        month, error_response = self.get_month_from_request(request)
        if error_response:
            return error_response

        house = get_object_or_404(House, id=house_id)
        year = month.year
        month_number = month.month
        results = CalculationResult.objects.filter(
            apartment__house_id=house_id,
            month__year=year,
            month__month=month_number
        )

        data = {
            'house': house,
            'apartment': results
        }
        serializer = ResultSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
