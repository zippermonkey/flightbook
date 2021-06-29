from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Flight(models.Model):
    name = models.CharField(max_length=200, null=True)
    start = models.CharField(max_length=200, null=True)
    end = models.CharField(max_length=200, null=True)
    departureTime = models.DateTimeField(null=False)
    capacity = models.IntegerField(null=False, default=120)
    purchased = models.IntegerField(default=0)
    price = models.FloatField(default=500)
    rownum = models.IntegerField(default=20)
    columnnum = models.IntegerField(default=6)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('未支付', '未支付'),
        ('已支付', '已支付'),
        ('已取票', '已取票'),
    )

    customer = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)


# 机票表
class Ticket(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, null=True, on_delete=models.CASCADE)
    seatrow = models.IntegerField(null=True)
    seatcolumn = models.IntegerField(null=True)

    class Meta:
        unique_together = (('customer', 'flight'),)
