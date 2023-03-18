from django.db import models
import uuid

# Create your models here.


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=200)
    amount = models.IntegerField()
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    transactionType = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
