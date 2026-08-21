# Automated Rental Market Monitor - To-Dos

## Session 1 (done)

- [x] Create GitHub repo (private, no license)
- [x] Initialize project with `uv` (not `pip`/`requirements.txt`)
- [x] Install `feedparser` and learn RSS parsing basics
- [x] Install `python-dotenv`
- [x] Run `uv audit` with clean results (no vulnerabilities)
- [x] Set `UV_MALWARE_CHECK=1`
- [x] Evaluate Craigslist RSS and drop due to ToS risk (see architecture)
- [x] Email Zillow, Redfin, StreetEasy,Apartments.com about personal-use policy
- [x] Confirm RentCast as sole data source

## Session 2 (next)

- [x] Sign up for RentCast and get a free Developer API key
- [x] Explore RentCast active listings endpoint (docs and API explorer)
- [x] Plan request budget to stay under 50 free requests/month on daily schedule
- [x] Write `src/fetch_rentcast.py` to pull active listings via `requests`
- [x] Design SQLite schema for `listings.db` (listings table + dedupe key)
- [x] Write `src/storage.py` insert/query logic using `INSERT OR IGNORE`
- [x] Implement core filters: max price $2,300, 2 bedrooms, 1 bathroom
- [x] Implement location filters: target neighborhoods and ZIP codes
- [x] Require listed address in the final match set
- [x] Build Google Maps link from address as a listing "link" substitute
- [x] Include listing agent contact info (name, phone, email) in each match

## Session 3

- [x] Write `src/email_digest.py` to generate HTML digest for new matches only
- [x] Send test digest email via Gmail SMTP (`smtplib` + app password)
- [x] Create `.github/workflows/weekly.yml` with daily cron schedule
- [] Add GitHub Secrets (RentCast API key, Gmail credentials)
- [x] Add Gmail app password (2-Step Verification + App Passwords page)
- [x] Send test digest email locally (uv run main.py)
- [x] Update .gitignore — stop ignoring listings.db (must persist across runs)
- [x] Manually trigger the Actions workflow, confirm it runs + emails successfully
- [x] Let Monday's scheduled run happen unattended, confirm it worked

## Later

- [] Add scam heuristics (suspiciously low price, no photos, boilerplate text)
- [] Add listing freshness filter (flag or deprioritize stale posts)
- [] Add broker fee and application fee mention flags
- [] Refine filter logic against real-world messy listing text
