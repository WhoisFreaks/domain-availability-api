"""Domain availability check with the WhoisFreaks Python SDK.

    pip install "whoisfreaks>=0.23.0"
    WHOISFREAKS_API_KEY=your_key python check_domain.py mybrand.com
"""
import os
import sys

import whoisfreaks

domain = sys.argv[1] if len(sys.argv) > 1 else "whoisfreaks.io"

config = whoisfreaks.Configuration()
config.api_key["ApiKeyAuth"] = os.environ["WHOISFREAKS_API_KEY"]

with whoisfreaks.ApiClient(config) as client:
    result = whoisfreaks.DomainAvailabilityApi(client).domain_availability_v2(domain)

print(result)
