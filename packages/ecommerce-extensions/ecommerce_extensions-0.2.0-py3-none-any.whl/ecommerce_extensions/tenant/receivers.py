"""Receiver file, contains all the methods which should be connected to a signal.

Receivers:
    update_tenant_settings: Connected to django.core.signals.request_started, will update
    the settings values.
"""
import logging

import six
from django.conf import settings as base_settings

from ecommerce_extensions.tenant.conf import TenantAwareSettings

LOG = logging.getLogger(__name__)


def update_tenant_settings(sender, environ, **kwargs):  # pylint: disable=unused-argument
    """
    Update the general django settings with the found values in TenantOptions.
    """
    http_host = environ.get("HTTP_HOST")

    if not http_host:
        LOG.warning("Could not find the host information.")
        return

    options = TenantAwareSettings.get_tenant_options(http_host)

    for key, value in six.iteritems(options):
        if isinstance(value, dict):
            merged = getattr(base_settings, key, {}).copy()
            merged.update(value)
            value = merged

        setattr(base_settings, key, value)
