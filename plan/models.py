from django.db import models
import uuid

# Create your models here.


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    words = models.CharField(max_length=200)
    isFree = models.BooleanField(default=False)
    amount = models.IntegerField()
    description = models.TextField(max_length=500, null=True, blank=True)
    isAvailable = models.BooleanField(default=True)
