from django.db import models
import uuid

# Create your models here.


class EmailTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.TextField(max_length=500, blank=True, null=True)
    isPopular = models.BooleanField(default=False)
    isAvailable = models.BooleanField(default=True)
    created_by = models.ForeignKey("account.User", on_delete=models.CASCADE)
