import pandas as pd
import numpy as np
import glob
import os
import zipfile
import warnings

main_folder = r"C:\Users\raymo\PycharmProjects\PropertyPriceScraper"
output_history = os.path.join(main_folder, "output_history")
filenames = glob.glob(output_history + "/*SOLD.csv")

# Define options and mappings
factor_options = ["suburb", "postcode", "property_type", "property_type_detail", "bedrooms", "bathrooms", "parking_spaces"] # Also the list of filters
aggregation_options = ["Daily", "Monthly", "Quarterly", "Half-Yearly", "Annually"]
aggregation_type = ["Mean", "Median", "Mode", "Min", "Max"]
aggregate_level_map = {"Daily": "sold_date", "Monthly": "sold_month", "Quarterly": "sold_quarter", "Half-Yearly": "sold_half_year", "Annually": "sold_year"}
aggregate_option_map = {"Mean": "mean_price", "Median": "median_price", "Mode": "mode_price", "Min": "min_price", "Max": "max_price"}

def aggregate_type_map(df):
    df = df.reset_index(drop=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mode_price = df["price"].mode()[0] if len(df["price"].mode()) > 0 else np.nan
        return pd.DataFrame({"mean_price": [df["price"].mean()], "median_price":  [df["price"].median()],
                             "mode_price":  [mode_price], "min_price":  [df["price"].min()],
                             "max_price":  [df["price"].max()], "count": [df["price"].count()]})

# Stack suburb level data into one aggregate dataframe
df_aggr = []
for file in filenames:
    df = pd.read_csv(file)
    df_aggr.append(df)
df_aggr = pd.concat(df_aggr, sort=False, ignore_index=True)

# Data cleaning
df_aggr["sold_date"] = pd.to_datetime(df_aggr["sold_date"])
df_aggr.drop_duplicates(inplace=True, ignore_index=True)
df_aggr = df_aggr.loc[df_aggr["sold_date"] >= "2000-01-01"] # Only keep entries after 2000-01-01
df_aggr["price"] = np.where(df_aggr["price"] >= 20000000, 20000000, df_aggr["price"]) # Cap price at 20m
df_aggr["bathrooms"] = np.where(df_aggr["bathrooms"] >= 20, 20, df_aggr["bathrooms"]) # Cap bathrooms at 25
df_aggr["bedrooms"] = np.where(df_aggr["bedrooms"] >= 20, 20, df_aggr["bedrooms"]) # Cap bedrooms at 25
df_aggr["parking_spaces"] = np.where(df_aggr["parking_spaces"] >= 10, 10, df_aggr["parking_spaces"]) # Cap parking_spaces at 25

drop_list = ["badge", "state", "full_address", "price_text", "listing_company_id", "listing_company_name", "auction_date", "available_date", "building_size", "land_size"]
df_aggr.drop(columns=drop_list, inplace=True)
df_aggr.to_csv(os.path.join(main_folder, "ALL_SOLD.csv"), index=False)
with zipfile.ZipFile(os.path.join(main_folder, "ALL_SOLD.zip"), 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(main_folder, "ALL_SOLD.csv"), arcname="ALL_SOLD.csv")