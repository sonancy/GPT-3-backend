from django.db import models
import uuid

# Create your models here.


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    file = models.FileField(max_length=255)
    wordCount = models.IntegerField()
    characterCount = models.IntegerField()
    texts = models.TextField(max_length=500, blank=True, null=True)
