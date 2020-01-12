from currency_converter_api.currency.models import Currency
from rest_framework import serializers


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ['symbol', 'rate', 'last_updated']
