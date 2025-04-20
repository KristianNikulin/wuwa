from rest_framework import serializers
from .models import ArbitrationCase

class ArbitrationCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrationCase
        fields = '__all__'
