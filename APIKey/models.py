from django.db import models
import uuid

# Create your models here.


class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    host = models.CharField(max_length=255)
    limit = models.IntegerField()
    isDisabled = models.BooleanField(default=False)
    disabledReason = models.TextField(max_length=500, blank=True, null=True)
