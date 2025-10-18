from rest_framework import serializers
from .models import ItemUsed

class ItemUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUsed
        fields = "__all__"