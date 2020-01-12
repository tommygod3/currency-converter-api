from django.shortcuts import render, get_object_or_404
from currency_converter_api.currency.models import Currency
from rest_framework import viewsets
from currency_converter_api.currency.serializers import CurrencySerializer
from rest_framework.response import Response

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('-symbol')
    serializer_class = CurrencySerializer
    
    def list(self, request, format=None):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        currency = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(currency)
        return Response(serializer.data)
