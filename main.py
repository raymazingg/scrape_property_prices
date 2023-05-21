
import json
from dataclasses import asdict
from realestate_com_au import RealestateComAu

api = RealestateComAu()

# Get property listings
listings = api.search(
    locations=["Edmondson Park, NSW 2171"], # search term
    channel="sold", # listing type
    sort_type="new-desc", # sort method
    limit=10, # number of articles to collect
    property_types = ["townhouse"],  # "house", "unit apartment", "townhouse", "villa", "land", "acreage", "retire", "unitblock""
    min_bedrooms = 1,
    max_bedrooms = 1
)