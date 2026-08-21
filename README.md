# Automated Rental Market Monitor

Personal automation project that checks NY rental listings weekly
against my own search criteria and emails me a digest of new matches


## How it works
1. GitHub Actions runs the pipeline every Monday (also manually
   triggerable from the Actions tab)
2. `fetch_rentcast.py` calls the RentCast API for each target Queens
   neighborhood
3. `storage.py` stores results in SQLite, deduping against previously
   seen listings and refreshing a `last_seen_at` timestamp on repeat
   sightings
4. `email_digest.py` builds an HTML digest of only the genuinely new
   listings
5. `send_email.py` sends it via Gmail SMTP

Each listing in the digest includes address, price, bed/bath count, a
Google Maps link (RentCast doesn't provide a source listing URL), and
the listing agent's contact info.

## Stack
Python 3, `uv`, `requests`, `sqlite3`, `smtplib`, `python-dotenv`,
GitHub Actions, GitHub Actions Secrets

## Search scope
Queens only — 10 target neighborhoods (Queens Village, Richmond Hill,
Springfield Gardens, Hillside, South Ozone Park, St. Albans, Cambria
Heights, Laurelton, Kew Gardens, Rego Park), max $2,000/month,
2bd/1ba.

## Security
- `uv audit` run before each session
- `UV_MALWARE_CHECK=1` enabled for dependency installs
- RentCast API key scoped to only the rental listings endpoint
- All secrets stored via GitHub Actions Secrets, never committed

## Status
In progress — Session 3 (email + scheduling) underway

## Data source decisions
See `architecture.md` for the full reasoning behind using RentCast as
the sole data source. Craigslist RSS, Zillow, Apartments.com, MLS
access, and Playwright scraping were all evaluated and ruled out.