from django.db import models
import uuid
from ingredient.models import Ingredient

class ItemUsed(models.Model):
    id = id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True , editable=False)
    quantity = models.IntegerField(default=0)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="iten_used")
    created_at = models.DateTimeField(auto_now_add=True)
