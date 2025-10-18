from django.db import models
import uuid
from enums.measurament import Measurament

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    measurament = models.CharField(choices=Measurament.choices, default=Measurament.GRAM, max_length=10)