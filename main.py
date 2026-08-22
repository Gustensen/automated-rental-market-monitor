from dotenv import load_dotenv
from src.db.storage import init_db, save_new_listings
from src.email_digest import build_digest_html
from src.fetch_rentcast import NEIGHBORHOODS, fetch_listings
from src.send_email import send_email


def main():
    # Load environment variables from .env for local runs.
    load_dotenv()

    conn = init_db()
    all_new_listings = []

    try:
        # Query each configured neighborhood and keep only brand-new rows.
        for city, state in NEIGHBORHOODS:
            listings = fetch_listings(
                city=city,
                state=state,
                price=2000,
                bedrooms=2,
                bathrooms=1,
            )
            newly_inserted = save_new_listings(conn, listings)
            all_new_listings.extend(newly_inserted)

        # Build digest HTML; returns None when there is nothing new to email.
        digest_html = build_digest_html(all_new_listings)

        if digest_html:
            send_email(digest_html, subject="New Rental Matches")
            print(f"Run complete: found {len(all_new_listings)} new listing(s). Digest email sent.")
        else:
            print("Run complete: no new listings found. No email sent.")
    finally:
        # Always close the DB connection, even if one neighborhood request fails.
        conn.close()


if __name__ == "__main__":
    main()
