// Domain availability check with the WhoisFreaks API. Node.js 18+ (built-in fetch).
// Usage: WHOISFREAKS_API_KEY=your_key node check-domain.mjs mybrand.com
const domain = process.argv[2] ?? "whoisfreaks.io";

const url = new URL("https://api.whoisfreaks.com/v2.0/domain/availability");
url.search = new URLSearchParams({
  domain,
  apiKey: process.env.WHOISFREAKS_API_KEY,
});

const res = await fetch(url);
if (!res.ok) {
  console.error(res.status, await res.text());
  process.exit(1);
}
console.log(await res.json());
