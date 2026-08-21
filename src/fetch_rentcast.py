import os
import requests
from dotenv import load_dotenv

# Load variables from .env into the environment (e.g. RENTCAST_API_KEY)
load_dotenv()

API_KEY = os.getenv("RENTCAST_API_KEY")
BASE_URL = "https://api.rentcast.io/v1/listings/rental/long-term"



def fetch_listings(price=2300, bedrooms=2, bathrooms=1, limit=50, city=None, state=None, zip_code=None):
    """
    Calls RentCast's active rental listings endpoint for one search area.
    Pass either (city, state) OR zip_code, not both.
    Returns a list of listing dicts (empty list if nothing matches).
    """
    # RentCast auth is a custom header, not a URL param or Bearer token
    headers = {"X-Api-Key": API_KEY}
    # Filters applied to every search area
    params = {
        "price": price,      # treated as a max when a single value is given
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "status": "Active",  # only currently-active listings, not removed/rented
        "limit": limit,      # max results per call (RentCast caps at 500 but it's safer to keep it lower at 50)
    }
    if zip_code:
        params["zipCode"] = zip_code
    else:
        params["city"] = city
        params["state"] = state

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status() # raises an exception instead of failing silently
    return response.json()

# 10 cities in total
NEIGHBORHOODS = [
    ("Laurelton", "NY"),("Queens Village", "NY") ,("Springfield Gardens", "NY"), ("Lynbrook", "NY"), ("Bellerose", "NY"),("St. Albans", "NY"),
    ("New Hyde Park", "NY"),("Cambria Heights", "NY"), ("Kew Gardens", "NY"),("Rego Park", "NY")]
