from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from currency_converter_api.currency import views

router = routers.DefaultRouter()
router.register(r'currency', views.CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
