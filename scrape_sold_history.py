import pandas as pd
import numpy as np
from realestate_com_au import RealestateComAu
from dataclasses import asdict
import os

main_folder = r"C:\Users\raymo\PycharmProjects\PropertyPriceScraper"
suburb_postcode_mapping_path = os.path.join(main_folder, r"sydney_suburb_postcode_mapping.csv")
keeplist = ["badge", "url", "suburb", "state", "postcode", "short_address", "full_address", "price", "price_text",
            "property_type", "bedrooms", "bathrooms", "parking_spaces", "building_size", "building_size_unit",
            "land_size", "land_size_unit", "listing_company_id", "listing_company_name", "auction_date",
            "available_date", "sold_date"]

suburb_postcode_mapping = pd.read_csv(suburb_postcode_mapping_path)

for i in range(len(suburb_postcode_mapping.index)):
    suburb = suburb_postcode_mapping["Suburb"][i]
    postcode = suburb_postcode_mapping["Postcode"][i]
    df_suburb = []
    for property_type in [["house"], ["unit apartment"], ["townhouse"], ["villa"], ["land"], ["acreage"], ["retire"], ["unitblock"]]:
        # Split houses, units & apartments, villas into number of rooms and aggregate to ensure all data is collected
        property_type_listings = []
        if property_type in [["house"], ["unit apartment"], ["townhouse"], ["villa"]]:
            for no_of_bedrooms in range(10):
                api = RealestateComAu()
                listings = api.search(
                    locations=[f"{suburb}, NSW {postcode}"], # search term
                    surrounding_suburbs=False,
                    channel="sold", # listing type
                    sort_type="new-desc", # sort methods
                    property_types=property_type,  # "house", "unit apartment", "townhouse", "villa", "land", "acreage", "retire", "unitblock""
                    min_bedrooms=no_of_bedrooms,
                    max_bedrooms=no_of_bedrooms,
                    limit=30000 # number of articles to collect
                )
                property_type_listings.extend(listings)
        else:
            api = RealestateComAu()
            listings = api.search(
                locations=[f"{suburb}, NSW {postcode}"],  # search term
                surrounding_suburbs=False,
                channel="sold",  # listing type
                sort_type="new-desc",  # sort methods
                property_types=property_type,
                limit=30000  # number of articles to collect
            )
            property_type_listings.extend(listings)

        # Transform output for property type into dataframe
        for j in property_type_listings:
            dict_listing = asdict(j)
            dict_listing_keep = {key: [dict_listing[key]] for key in keeplist}
            df_listing = pd.DataFrame.from_dict(dict_listing_keep)
            df_listing.rename({"property_type": "property_type_detail"}, axis="columns", inplace=True)
            df_listing["property_type"] = property_type[0]
            df_suburb.append(df_listing)

    # Only concatenate and write suburb level history to csv
    if len(df_suburb) > 0:
        df_suburb = pd.concat(df_suburb, sort=False, ignore_index=True)
        df_suburb["building_size_clean"] = np.where(df_suburb["building_size_unit"]=="ha", df_suburb["building_size"] * 10000, df_suburb["building_size"])
        df_suburb["land_size_clean"] = np.where(df_suburb["land_size_unit"] == "ha", df_suburb["land_size"] * 10000, df_suburb["land_size"])
        df_suburb.to_csv(os.path.join(main_folder, "output_history", f"{suburb}_{postcode}_SOLD.csv"), index=False)

