# Domain Availability API: Check if a Domain Is Available

Check whether a domain name is available to register with the [WhoisFreaks Domain Availability API](https://whoisfreaks.com/products/domain-availability-api), a REST API you can call from any language. Ask about one domain, get up to 100 available alternatives on other TLDs in the same call, or check up to 100 domains in one bulk request.

This page uses plain HTTP and the official [Python SDK](https://github.com/WhoisFreaks/whoisfreaks-python). Ready-to-run scripts in cURL, Python and Node.js are in [`examples/`](examples/). The same API key works for WHOIS, DNS lookup and the other WhoisFreaks APIs.

A check for `whoisfreaks.com` returns this complete response:

```json
{
  "domain": "whoisfreaks.com",
  "availability": "UNAVAILABLE"
}
```

## Contents

- [Quick start](#quick-start)
- [Check one domain](#check-one-domain)
- [Get suggestions on other TLDs](#get-suggestions-on-other-tlds)
- [Bulk domain availability check](#bulk-domain-availability-check)
- [Parameters and response fields](#parameters-and-response-fields)
- [Use cases](#use-cases)
- [Errors and rate limits](#errors-and-rate-limits)
- [Credits](#credits)
- [FAQ](#faq)
- [Other languages and related APIs](#other-languages-and-related-apis)

## Quick start

**1. Install the SDK** (Python 3.8 or later):

```sh
pip install "whoisfreaks>=0.23.0"
```

**2. Get an API key.** Create a free account at [billing.whoisfreaks.com/signup](https://billing.whoisfreaks.com/signup). New accounts get 500 free credits with no credit card.

**3. Keep the key out of your code.** Export it as an environment variable:

```sh
export WHOISFREAKS_API_KEY="your_api_key"
```

**4. Configure the client once.** Every example below starts from this setup:

```python
import os
import whoisfreaks

config = whoisfreaks.Configuration()
config.api_key["ApiKeyAuth"] = os.environ["WHOISFREAKS_API_KEY"]
```

## Check one domain

```python
with whoisfreaks.ApiClient(config) as client:
    api = whoisfreaks.DomainAvailabilityApi(client)
    result = api.domain_availability_v2("whoisfreaks.com")

    print(result.domain, result.availability)   # whoisfreaks.com UNAVAILABLE
```

The same request over plain HTTP:

```sh
curl "https://api.whoisfreaks.com/v2.0/domain/availability?domain=whoisfreaks.com&apiKey=$WHOISFREAKS_API_KEY"
```

## Get suggestions on other TLDs

When the name you want is taken, turn on suggestions. The API checks the same name on other TLDs and returns up to 100 alternatives, with the availability of each.

```python
with whoisfreaks.ApiClient(config) as client:
    api = whoisfreaks.DomainAvailabilityApi(client)
    result = api.domain_availability_v2("whoisfreaks.com", sug=True, count=10)

    for suggestion in result.domain_available_response or []:
        print(suggestion.domain, suggestion.availability)
```

With suggestions on, the response is one list, `domain_available_response`, with the availability of every name checked, including the one you asked about. `count` sets how many names to return, from 1 to 100 (default 5). Suggestions cost 1 extra credit per 5, so `count=10` costs 3 credits in total.

<details>
<summary>Example response for whoisfreaks.com with count=10</summary>

```json
{
  "domain_available_response": [
    {
      "domain": "whoisfreaks.xyz",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.net",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.club",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.com",
      "availability": "UNAVAILABLE"
    },
    {
      "domain": "whoisfreaks.info",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.loan",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.org",
      "availability": "UNAVAILABLE"
    },
    {
      "domain": "whoisfreaks.dev",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.top",
      "availability": "AVAILABLE"
    },
    {
      "domain": "whoisfreaks.biz",
      "availability": "AVAILABLE"
    }
  ]
}
```

</details>

## Bulk domain availability check

Check up to 100 domains in one request. Useful for a shortlist of brand names, a list of domains you want to buy, or a nightly check of names you are watching.

```python
with whoisfreaks.ApiClient(config) as client:
    request = whoisfreaks.BulkDomainAvailabilityRequest(
        domain_names=["whoisfreaks.com", "whoisfreaks.io", "whoisfreaks.ai"]
    )
    result = whoisfreaks.DomainAvailabilityApi(client).bulk_domain_availability_v2(request)

    for item in result.bulk_domain_availability_response or []:
        print(item.domain, item.availability)
```

<details>
<summary>Example response</summary>

```json
{
  "bulk_domain_availability_response": [
    {
      "domain": "whoisfreaks.com",
      "availability": "UNAVAILABLE",
      "status": true
    },
    {
      "domain": "whoisfreaks.ai",
      "availability": "AVAILABLE",
      "status": true
    },
    {
      "domain": "whoisfreaks.io",
      "availability": "AVAILABLE",
      "status": true
    }
  ]
}
```

</details>

Over plain HTTP, the domains go in a JSON body:

```sh
curl -X POST "https://api.whoisfreaks.com/v2.0/domain/availability?apiKey=$WHOISFREAKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domainNames": ["whoisfreaks.com", "whoisfreaks.io", "whoisfreaks.ai"]}'
```

## Parameters and response fields

Single check, `GET /v2.0/domain/availability`:

| Parameter | Required | Description |
|---|---|---|
| `domain` | yes | The domain to check, for example `whoisfreaks.com` |
| `sug` | no | `true` to return suggestions on other TLDs. Default `false` |
| `count` | no | Number of suggestions when `sug` is `true`, 1 to 100. Default `5` |
| `format` | no | `json` (default) or `xml` |

Bulk check, `POST /v2.0/domain/availability`: send `{"domainNames": [...]}` with up to 100 domains.

| Response field | Description |
|---|---|
| `domain` | The domain that was checked |
| `availability` | `AVAILABLE` or `UNAVAILABLE` |
| `domain_available_response` | Returned instead of the two fields above when `sug` is `true`: one `domain` and `availability` per name checked, including the one you asked about |
| `bulk_domain_availability_response` | Bulk results: one `domain`, `availability` and `status` (`true` when the check succeeded) per domain |

## Use cases

**Domain search box.** Power the "is it available?" field on a registrar, hosting or website builder signup page, and show alternatives on other TLDs when the first choice is taken.

**Brand and product naming.** Check a shortlist of names in one bulk request before you commit to one, so the matching domain is still free when you launch.

**Domain watchlist.** Re-check a list of taken domains on a schedule and get alerted when one becomes available:

```python
watchlist = ["whoisfreaks.ai", "whoisfreaks.dev"]

with whoisfreaks.ApiClient(config) as client:
    result = whoisfreaks.DomainAvailabilityApi(client).bulk_domain_availability_v2(
        whoisfreaks.BulkDomainAvailabilityRequest(domain_names=watchlist)
    )

available = [
    item.domain
    for item in result.bulk_domain_availability_response or []
    if (item.availability or "").upper() == "AVAILABLE"
]
print("Now available:", available)
```

For domains that are taken, the [WHOIS API](https://github.com/WhoisFreaks/whois-api) tells you who holds them and when they expire.

## Errors and rate limits

Failed requests raise `ApiException` with the HTTP status code and the response body:

```python
from whoisfreaks.rest import ApiException

with whoisfreaks.ApiClient(config) as client:
    try:
        result = whoisfreaks.DomainAvailabilityApi(client).domain_availability_v2("whoisfreaks.com")
    except ApiException as e:
        print(e.status, e.body)
```

| Status | Meaning |
|---|---|
| 401 | Missing, invalid or suspended API key |
| 429 | Rate limit reached for this minute |

Rate limits are counted per minute, per endpoint category, and depend on your plan. A request that is throttled does not use a credit. Every response carries `x-ratelimit-allowed-requests`, `x-ratelimit-remaining-requests` and `x-ratelimit-remaining-time` (time until the window resets, in nanoseconds). The `_with_http_info` variant of each method returns these headers:

```python
with whoisfreaks.ApiClient(config) as client:
    response = whoisfreaks.DomainAvailabilityApi(client).domain_availability_v2_with_http_info(
        "whoisfreaks.com"
    )
    print(response.headers.get("x-ratelimit-remaining-requests"))
    result = response.data
```

On a 429, wait until `x-ratelimit-remaining-time` has passed, plus a small buffer, then retry. See [API rate limiting](https://whoisfreaks.com/documentation/api-rate-limiting).

## Credits

| Request | Credits |
|---|---|
| One domain, no suggestions | 1 |
| Suggestions | 1 more per 5 suggestions |

Full pricing: [credit usage](https://whoisfreaks.com/documentation/credit-usage).

## FAQ

**Is the availability check real time?**
Yes. The API checks registration status in real time when you call it.

**Is there a free domain availability API?**
Yes. A [free WhoisFreaks account](https://whoisfreaks.com/products/whois-api/free-whois-api) includes 500 credits with no credit card. The credits never expire, and free keys can be used commercially.

**How many suggestions can I get?**
Up to 100 per request, set with `count`.

**How many domains can I check at once?**
Up to 100 per bulk request. For more, split the list into batches of 100.

**Can I get XML instead of JSON?**
Yes. Pass `format="xml"` in Python or `&format=xml` over HTTP.

## Other languages and related APIs

The Domain Availability API has official SDKs for [Python](https://github.com/WhoisFreaks/whoisfreaks-python), [JavaScript](https://github.com/WhoisFreaks/whoisfreaks-javascript), [TypeScript](https://github.com/WhoisFreaks/whoisfreaks-typescript), [Java](https://github.com/WhoisFreaks/whoisfreaks-java), [Kotlin](https://github.com/WhoisFreaks/whoisfreaks-kotlin), [Go](https://github.com/WhoisFreaks/whoisfreaks-go), [C#](https://github.com/WhoisFreaks/whoisfreaks-csharp), [Ruby](https://github.com/WhoisFreaks/whoisfreaks-ruby), [PHP](https://github.com/WhoisFreaks/whoisfreaks-php) and [Swift](https://github.com/WhoisFreaks/whoisfreaks-swift).

Related quick starts with the same API key:

- [WHOIS API](https://github.com/WhoisFreaks/whois-api): live, historical, reverse and bulk WHOIS
- [DNS lookup API](https://github.com/WhoisFreaks/dns-lookup-api): live, historical and reverse DNS records

Documentation: [domain availability API](https://whoisfreaks.com/documentation/domain-availability-api). Questions: support@whoisfreaks.com.
