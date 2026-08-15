# Automated Rental Market Monitor - To-Dos

## Session 1 (done)

- [x] Create GitHub repo (private, no license)
- [x] Initialize project with `uv` (not `pip`/`requirements.txt`)
- [x] Install `feedparser` and learn RSS parsing basics
- [x] Install `python-dotenv`
- [x] Run `uv audit` with clean results (no vulnerabilities)
- [x] Set `UV_MALWARE_CHECK=1`
- [x] Evaluate Craigslist RSS and drop due to ToS risk (see architecture)
- [x] Email Zillow, Redfin, StreetEasy, and Apartments.com about personal-use policy
- [x] Confirm RentCast as sole data source

## Session 2 (next)

- [x] Sign up for RentCast and get a free Developer API key
- [x] Explore RentCast active listings endpoint (docs and API explorer)
- [x] Plan request budget to stay under 50 free requests/month on daily schedule
- [x] Write `src/fetch_rentcast.py` to pull active listings via `requests`
- [] Design SQLite schema for `listings.db` (listings table + dedupe key)
- [] Write `src/storage.py` insert/query logic using `INSERT OR IGNORE`
- [x] Implement core filters: max price $2,000, 2 bedrooms, 1 bathroom
- [] Implement location filters: target neighborhoods and ZIP codes
- [] Require listed address in the final match set
- [] Parse utilities included/excluded from descriptions using regex (`re`)

## Session 3

- [] Write `src/email_digest.py` to generate HTML digest for new matches only
- [] Send test digest email via Gmail SMTP (`smtplib` + app password)
- [] Create `.github/workflows/daily.yml` with daily cron schedule
- [] Add GitHub Secrets (RentCast API key, Gmail credentials)
- [] Run end-to-end test (manual trigger first, then live cron)

## Phase 2 / later

- [] Add scam heuristics (suspiciously low price, no photos, boilerplate text)
- [] Add listing freshness filter (flag or deprioritize stale posts)
- [] Add broker fee and application fee mention flags
- [] Refine filter logic against real-world messy listing text
- [] Optional: integrate Zillow Research aggregate market stats (non-listing context)
- [] Revisit Redfin/StreetEasy only if they grant licensed personal-use access
- [] Keep out of scope: Apartments.com (denied), MLS (license required), Playwright scraping (no clear permission)
