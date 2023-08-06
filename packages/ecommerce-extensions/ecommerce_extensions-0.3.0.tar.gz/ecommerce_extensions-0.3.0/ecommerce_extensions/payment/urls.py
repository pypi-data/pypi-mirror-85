"""Payment processors urls file."""
from django.urls import path

from ecommerce_extensions.payment.views import fomopay, payu

PAYU_URLS = [
    path("notify/", payu.PayUPaymentResponseView.as_view(), name="notify"),
]

FOMOPAY_URLS = [
    path("notify/", fomopay.FomopayPaymentResponseView.as_view(), name='notify'),
    path("pay/", fomopay.FomopayQRView.as_view(), name='payment'),
    path("status/", fomopay.FomopayPaymentStatusView.as_view(), name='status')
]
