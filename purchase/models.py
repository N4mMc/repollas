from django.db import models
from ingredient.models import Ingredient
from order.models import Order
import uuid

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField(blank=False, null=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="purchases")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="purchases")