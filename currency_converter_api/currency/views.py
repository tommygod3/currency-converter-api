from django.shortcuts import render, get_object_or_404
from currency_converter_api.currency.models import Currency
from rest_framework import viewsets
from currency_converter_api.currency.serializers import CurrencySerializer
from rest_framework.response import Response

import json
import requests
from datetime import datetime, timezone, timedelta

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('-symbol')
    serializer_class = CurrencySerializer

    api_url = "http://apilayer.net/api/live?access_key=2938f0796b94b63bdd3d56e0faa2628e"

    def update_all_currencies(self):
        content = requests.get(self.api_url).content
        api_dict = json.loads(content)

        for symbol, usd_rate in api_dict["quotes"].items():
            if symbol == "USDGBP":
                usd_gbp_rate = usd_rate

        for symbol, usd_rate in api_dict["quotes"].items():
            data = {
                "gbp_rate": usd_rate/usd_gbp_rate,
                "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
            }

            try:
                obj = Currency.objects.get(symbol=symbol[3:])
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()

            except Currency.DoesNotExist:
                new_values = {"symbol": symbol[3:]}
                new_values.update(data)
                obj = Currency(**new_values)
                obj.save()
    
    def list(self, request, format=None):
        for currency in self.queryset:
            if datetime.now(timezone.utc) - currency.last_updated > timedelta(days=7):
                self.update_all_currencies()
                break

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        currency = get_object_or_404(self.queryset, pk=pk)

        if datetime.now(timezone.utc) - currency.last_updated > timedelta(days=1):
            content = requests.get(self.api_url+"&currencies=GBP").content
            gbp_dict = json.loads(content)
            usd_gbp_rate = gbp_dict["quotes"]["USDGBP"]

            params = f"&currencies={pk}"

            content = requests.get(self.api_url+params).content
            api_dict = json.loads(content)

            gbp_rate = api_dict["quotes"][f"USD{pk}"] / usd_gbp_rate

            currency.gbp_rate = gbp_rate
            currency.last_updated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
            currency.save()
  

        serializer = self.serializer_class(currency)
        return Response(serializer.data)
