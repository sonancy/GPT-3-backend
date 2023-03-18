from django.db import models
import uuid

# Create your models here.


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    isFolder = models.BooleanField(default=False)
    parentFolder = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    description = models.TextField(max_length=500, blank=True, null=True)
    size = models.IntegerField()
