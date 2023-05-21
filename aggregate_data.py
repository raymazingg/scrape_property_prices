import pandas as pd
import glob
import os

main_folder = r"C:\Users\raymo\PycharmProjects\PropertyPriceScraper"
output_history = os.path.join(main_folder, "output_history")
filenames = glob.glob(output_history + "/*SOLD.csv")

df_aggr = []
for file in filenames:
    df = pd.read_csv(file)
    df_aggr.append(df)

df_aggr = pd.concat(df_aggr, sort=False, ignore_index=True)
df_aggr.to_csv(os.path.join(main_folder, "ALL_SOLD.csv"), index=False)