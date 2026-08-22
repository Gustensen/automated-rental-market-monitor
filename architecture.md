# Automated Rental Market Monitor - Architecture

## Purpose

Automate a daily rental search workflow: fetch active listings, dedupe against prior runs, filter by personal criteria, and email only new matching listings.

## End-to-End Pipeline

1. GitHub Actions (daily cron schedule) triggers the run.
2. `src/fetch_rentcast.py` calls the RentCast active listings endpoint using `requests`.
3. `src/storage.py` writes listings into SQLite (`listings.db`) with `INSERT OR IGNORE` to dedupe previously seen listings.
4. New listings are filtered against configured criteria.
5. `src/email_digest.py` builds an HTML digest containing only new matches.
6. `smtplib` sends the digest via Gmail SMTP to the inbox.

## ASCII Flow Diagram

```text
+-----------------------------+
| GitHub Actions (daily cron) |
+-------------+---------------+
              |
              v
+-----------------------------+
| fetch_rentcast.py           |
| - requests -> RentCast API  |
| - active listings endpoint  |
+-------------+---------------+
              |
              v
+-----------------------------+
| storage.py + SQLite         |
| listings.db                 |
| INSERT OR IGNORE (dedupe)   |
+-------------+---------------+
              |
              v
+-----------------------------+
| Filter Engine               |
| - criteria + regex parsing  |
| - keep only new matches     |
+-------------+---------------+
              |
              v
+-----------------------------+
| email_digest.py             |
| - build HTML digest         |
+-------------+---------------+
              |
              v
+-----------------------------+
| Gmail SMTP (smtplib)        |
| -> send digest to inbox     |
+-----------------------------+
```

## Tech Stack

- Python 3
- `uv` for dependency management (no `pip` + `requirements.txt` workflow)
- `requests` for HTTP calls to RentCast
- `sqlite3` (stdlib) for local persistence and dedupe
- `re` (stdlib) for utilities/fee keyword parsing
- `smtplib` + `email.mime` (stdlib) for SMTP email delivery
- `python-dotenv` for local secret loading
- GitHub Actions Secrets for CI secret injection
- `logging` (stdlib) for operational logs
- GitHub Actions YAML workflow as scheduler
- Dependency security: `uv audit` + `UV_MALWARE_CHECK=1`

## Filter Criteria

- Price: maximum $2,000
- Bedrooms: 2
- Bathrooms: 1
- Utilities included/excluded status parsed from listing description
- Target neighborhoods and ZIP codes
- Must include a listed address
- Listing freshness checks
- Scam heuristics (for example: suspiciously low price, no photos)
- Broker fee and application fee mention flags

## Data Source Decisions

| Source               | Decision           | Reasoning                                                                                                                     |
| -------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| RentCast API         | Keep (sole source) | Free tier (50 requests/month), licensed access, active listings endpoint, no known ToS conflict for this use.                 |

## Current Repo Layout

```text

├── .github/workflows
     ├── weekly.yml
├── src/
|    ├──db/
|        ├──listings.db
|        ├──storage.py
│   ├── fetch_rentcast.py
│   ├── storage.py
│   └── email_digest.py
    ├── send_email.py
├── main.py
├── .env (gitignored)
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```
