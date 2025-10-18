from django.db import models

class Measurament(models.TextChoices):
    MILILITER = "ml"
    UNIT = "u"
    GRAM = "gm"