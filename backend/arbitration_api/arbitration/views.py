from rest_framework import viewsets
from .models import ArbitrationCase
from .serializers import ArbitrationCaseSerializer

class ArbitrationCaseViewSet(viewsets.ModelViewSet):
    queryset = ArbitrationCase.objects.all()
    serializer_class = ArbitrationCaseSerializer
