import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RENTCAST_API_KEY")
BASE_URL = "https://api.rentcast.io/v1/listings/rental/long-term"


def fetch_listings(city, state, price, bedrooms, bathrooms, limit):
    headers = {"X-Api-Key": API_KEY}
    params = {
        "city": city,
        "state": state,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "status": "Active",
        "limit": limit
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json()


 # (city_or_neighborhood, state)
NEIGHBORHOODS = [("Queens Village", "NY"), ("Richmond Hill", "NY")]#("Jamaica", "NY"),  ("Springfield Gardens", "NY"), ("Hillside", "NY"), ("South Ozone Park", "NY"), ("St. Albans", "NY"), ("Cambria Heights", "NY"), ("Laurelton", "NY"), ("Kew Gardens", "NY"), ("Rego Park", "NY")]

if __name__ == "__main__":
    all_listings = []
    for city, state in NEIGHBORHOODS:
        listings = fetch_listings(city=city, state=state, price=2000, bedrooms=2, bathrooms=1, limit=50)
        print(f"{city}, {state}: {len(listings)} listings")
        all_listings.extend(listings)