from django.db import models

# Create your models here.
class Accounts(models.Model):
    acc_no=models.IntegerField(unique=True)
    choices = [
        ("savings", "savings"),
        ("current", "current")
    ]
    acc_type=models.CharField(max_length=10,choices=choices)
    bal=models.FloatField(default=0)
    user=models.CharField(max_length=10)

class transactions(models.Model):
    fromacc=models.IntegerField()
    toacc=models.IntegerField()
    amt=models.IntegerField()
    trdate=models.DateTimeField(auto_now=True)
