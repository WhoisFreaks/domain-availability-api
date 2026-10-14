#!/usr/bin/env sh
# Check if a domain is available, with 5 suggestions on other TLDs.
# Usage: WHOISFREAKS_API_KEY=your_key ./check-domain.sh mybrand.com
DOMAIN="${1:-whoisfreaks.io}"
curl -s "https://api.whoisfreaks.com/v2.0/domain/availability?domain=${DOMAIN}&sug=true&count=5&apiKey=${WHOISFREAKS_API_KEY}"
