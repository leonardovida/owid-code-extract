# %%
import os

import pandas as pd
from cleaner import read_and_clean_file

# %% tags=["parameters"]
upstream = None
product = None
gdrive_landing = None
mappings = None
mappings_xlsx = None

# %%
# Set mappings
CIRCLE_SIZES = {
    "small": 3,
    "normal": 5,
    "large": 10,
    "very_large": 50,
    "crazy_large": 100,
}

# %%
# Get mappings
read_file = pd.read_excel(mappings_xlsx, sheet_name="Data")
read_file.to_csv(mappings, index=None, header=True)

# Read CITIES MAPPINGS and modify variables
CITIES_MAPPING = pd.read_csv(mappings)
CITIES_MAPPING["city_name"] = CITIES_MAPPING["city_name"].str.lower()
CITIES_MAPPING["city_english_name"] = CITIES_MAPPING["city_english_name"].str.lower()

# %%
# Read and cleans the list of files in development
landing = gdrive_landing

res = []
files = os.listdir(landing)
for file in files:
    filename, file_extension = os.path.splitext(file)
    if file.endswith(".txt"):
        file_path = os.path.join(landing, file)
        if isinstance(file_path, str):
            try:
                cleaned_file = read_and_clean_file(
                    file_path=file_path, CITIES_MAPPING=CITIES_MAPPING, CIRCLE_SIZES=CIRCLE_SIZES
                )
                res.append(cleaned_file)
            except Exception as e:
                print(f"Cleaning file {file_path} failed with error {e}")
                raise

# %%
# Create df and PK
df = sum(res, [])
df = pd.DataFrame(df)
df["Key"] = df[["RecommendedPlace", "RecommendedCity", "Recommender"]].apply("_".join, axis=1)

# %%
# Save to pickle cleaned DataFrame
df.to_pickle(product["data"])
