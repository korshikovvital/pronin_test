from django.db import models


class Transaction(models.Model):
    customer = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'



    def __str__(self):
        return f"{self.customer} - {self.item} - {self.total}"



