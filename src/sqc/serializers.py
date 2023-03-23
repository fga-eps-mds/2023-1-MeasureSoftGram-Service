from django.utils import timezone
from rest_framework import serializers

from sqc.models import SQC


class SQCSerializer(serializers.ModelSerializer):
    """
    Serializadora usada para serializar as medidas calculadas
    """
    class Meta:
        model = SQC
        fields = (
            'id',
            'value',
            'created_at',
        )
        read_only_fields = (
            'id',
            'value',
        )


class SQCCalculationRequestSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(default=timezone.now)
