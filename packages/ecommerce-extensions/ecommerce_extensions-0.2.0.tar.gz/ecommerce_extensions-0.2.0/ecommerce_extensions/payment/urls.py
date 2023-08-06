"""Payment processors urls file."""
from django.urls import path

from ecommerce_extensions.payment.views import payu

PAYU_URLS = [
    path(r"^notify/$", payu.PayUPaymentResponseView.as_view(), name="notify"),
]
