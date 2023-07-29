import io
import csv

from rest_framework import status
from rest_framework.views import Response, APIView

from .models import Transaction
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


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
                        return Response(
                            'This data is already in the database',
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        data.save()

                return Response(
                    'Record added to database',
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'Status': 'Error', 'Desc': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        top_customers = Transaction.objects.values(
            'customer'
        ).annotate(
            spent_money=Sum('total')
        ).order_by(
            '-spent_money')[:5]

        gem_list = Transaction.objects.filter(
            customer__in=[customer['customer'] for customer in top_customers]
        ).values(
            'item'
        ).annotate(count=Count('customer')
                   ).filter(count__gte=2
                            ).values_list('item', flat=True)
        response = []
        for customer in top_customers:
            customer_data = {
                'username': customer['customer'],
                'spent_money': customer['spent_money'],
                'gems': gem_list,
            }
            response.append(customer_data)
        return Response({"response": response})
