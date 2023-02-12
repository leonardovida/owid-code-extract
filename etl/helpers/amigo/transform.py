import geopy.distance
import pandas as pd

from etl.config import CITIES_MAPPING


def transform(df: pd.DataFrame):
    """Transform the data retrieved from the amigo API."""
    cities_mappings = get_mappings()

    df = df.drop_duplicates(subset=["id"])

    # Clean data
    for col in ["typesData", "categories", "guidePicks", "notes.items"]:
        df[col] = df[col].apply(lambda x: x[0] if x else "None").astype(str)

    # Add distance from center
    for city_name in df["city_name"].unique():
        city_mapping = cities_mappings.loc[cities_mappings["city_name"] == city_name]
        city_center = city_mapping["center"].iloc[0]
        df.loc[df["city_name"] == city_name, "coordinates"] = city_center

    # Distance from center
    df["distance_from_center"] = df.apply(
        lambda row: geopy.distance.distance(
            (row["city_center"][0], row["city_center"][1]),
            (row["coordinates"][0], row["coordinates"][1]),
        ).km,
        axis=1,
    )

    # Filter by restaurant
    df["typesData"] = df["typesData"].str.lower()
    df["is_restaurant"] = df["typesData"].str.contains("restaurant")
    df = df[df["is_restaurant"] == True]

    return df


def get_mappings():
    """Get mapping file."""
    read_file = pd.read_excel(CITIES_MAPPING, sheet_name="Data")
    return read_file
