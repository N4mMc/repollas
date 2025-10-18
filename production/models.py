from django.db import models
import uuid
from item_used.models import ItemUsed

class Production(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True , editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    repollas = models.IntegerField(default=0)
    boxes = models.IntegerField(default=0)
    sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_used = models.ManyToManyField(ItemUsed, related_name="productions")
