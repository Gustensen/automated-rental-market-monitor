import sqlite3

DB_PATH = "listings.db"

def init_db():
    """
    Opens (or creates) the SQLite database and makes sure the listings
    table exists. Safe to call every run.
    """
    conn = sqlite3.connect(DB_PATH)
    # id helps dedup listings by making it the primary key. last_seen_date is updated every time we see a listing, so we can tell which listings are new vs. old.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            price INTEGER,
            bedrooms INTEGER,
            bathrooms INTEGER,
            property_type TEXT,
            status TEXT,
            listed_date DATE,
            agent_name TEXT,
            agent_phone TEXT,
            agent_email TEXT,
            last_seen_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def save_new_listings(conn, listings):
    """
    Takes one batch of listings from a single fetch_listings() call.
    - Skips listings with no address (nothing to verify/visit).
    - Brand-new listings: inserted, added to the returned "new" list (for the email).
    - Already-known listings: just get last_seen_at refreshed, not re-emailed.
    Returns only the genuinely new listings from this batch.
    """
    new_listings = []
    for listing in listings:
        if not listing.get("formattedAddress"):
            continue  # skip listings with no address

        listing_id = listing.get("id")
        cursor = conn.execute("SELECT 1 FROM listings WHERE id = ?", (listing_id,))
        already_known = cursor.fetchone() is not None

        if already_known:
        # Seen before — just prove it's still active by updating the timestamp
            conn.execute(
                "UPDATE listings SET last_seen_date = CURRENT_TIMESTAMP WHERE id = ?",(listing_id,)
            )
        else:
            # First time seeing this one — insert and flag as new for the digest
            agent = listing.get("listingAgent") or {}
            conn.execute("""
                INSERT INTO listings (id, address, city, state, zip_code,
                    price, bedrooms, bathrooms, property_type, status, listed_date, agent_name, agent_phone, agent_email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                listing.get("id"), listing.get("formattedAddress"),
                listing.get("city"), listing.get("state"), listing.get("zipCode"),
                listing.get("price"), listing.get("bedrooms"), listing.get("bathrooms"),listing.get("propertyType"), listing.get("status"), (listing.get("listedDate")),agent.get("name"), agent.get("phone"), agent.get("email")
            ))
            new_listings.append(listing)
    conn.commit()
    return new_listings