import googlemaps
import pandas as pd
import pendulum
from google_maps import find_places
from tqdm import tqdm

from etl.config import GOOGLE_KEY

upstream = ["clean-new-recommendations"]
product = None

incremental = True
tqdm.pandas()

# Get previous df, if not exists skip
if incremental:
    df_previous = pd.read_pickle(product["data"])
    # df_previous["Key"] = df_previous[["RecommendedPlace", "RecommendedCity",
    # "Recommender"]].apply("_".join, axis=1)
    df = pd.read_pickle(upstream["clean-new-recommendations"]["data"])
else:
    df = pd.read_pickle(upstream["clean-new-recommendations"]["data"])

if incremental:
    key_diff = set(df.Key).difference(df_previous.Key)
    where_diff = df.Key.isin(key_diff)
    df_diff = df[where_diff]
    print(df_diff.shape[0])

if incremental:
    df = df_diff
gmaps = googlemaps.Client(key=GOOGLE_KEY)
date = pendulum.today().to_date_string()

df[
    [
        "business_status",
        "formatted_address",
        "name",
        "global_code",
        "price_level",
        "rating",
        "types",
        "user_ratings_total",
        "status",
    ]
] = df.progress_apply(lambda row: find_places(row, gmaps), axis=1)

# TODO: filter out rows that are empty

if incremental:
    df_previous = df_previous.append(df_diff, ignore_index=True)


df.to_pickle(product["data"])
df.to_excel(product["excel"])
