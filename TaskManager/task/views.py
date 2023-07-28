import io
import csv

from rest_framework import status
from rest_framework.views import Response, APIView

from .models import Transaction


# @api_view(["POST"])
# def get_file(request):
#     file =request.FILES['file']
#     print(file)
#     if request.method == 'POST':
#         return Response({'message': 'Получены данные', 'data': request.data})


class DealsView(APIView):
    def post(self, request):
        try:
            file = request.FILES['file']
            with io.StringIO(file.read().decode()) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data = Transaction(
                        customer=row['customer'],
                        item=row['item'],
                        total=row['total'],
                        quantity=row['quantity'],
                        date=row['date'])
                    if Transaction.objects.filter(
                            customer=row['customer'],
                            item=row['item'],
                            total=row['total'],
                             quantity=row['quantity'],
                            date=row['date']).exists():
                        return Response('This data is already in the database', status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data.save()

                return Response('Record added to database', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
