import time

import pandas as pd
import requests

from etl.config import AMIGO_BEARER_TOKEN, AMIGO_PLACES_DF, AMIGO_PORT, AMIGO_URL
from etl.helpers.amigo.query import query_get_places


def extract(df_cities: pd.DataFrame):
    """Extract data from API

    Args:
        df_cities (pd.DataFrame): The dataframe containing the cities to be
            extracted from the API.

    Returns:
        pd.DataFrame: The dataframe containing the places extracted from the API.
    """
    if AMIGO_PLACES_DF is not None:
        df_places = pd.read_parquet(AMIGO_PLACES_DF)
    else:
        df_places = None

    try:
        # Iterate over all cities in the df_cities dataframe
        for index, row in df_cities.iterrows():
            print(f"City {index} : {row[0]}, {row[2]}, {row[17]}")

            df_temp = get_places(name=row[2], city_id=str(row[0]), region=row[17])

            # if df is None, skip the rest of the loop
            if df_temp is None:
                continue
            # if df_existing is defined, append the df_temp to df_existing
            if index != 1:
                df_places = pd.concat([df_places, df_temp], ignore_index=True)
            # if df_places is not defined, df_places = df
            else:
                df_places = df_temp

            time.sleep(0.1)

            # Concatenate the df_places dataframe with the df_temp dataframe
            df_places = pd.concat([df_places, df_temp], ignore_index=True)

        return df_places

    except Exception:
        print("There has been a problem in the extraction.")
        return df_places


def get_places(name: str, city_id: str, region: str, last: str = "None", df_places=None):
    """Get places from API, this function can be called recursively

    Args:
        name (str): The name of the city
        city_id (str): The city ID
        region (str): The region to which the city being extracted belongs to
        df_places (pd.DataFrame, optional): The dataframe containing the places

    Raises:
        ValueError: If AMIGO_BEARER_TOKEN is not defined

    Returns:
        pd.DataFrame: The dataframe containing the extracted places
    """
    if last == "None":
        json_data = {
            "operationName": "ExplorePlacesExploreRadius",
            "query": query_get_places,
            "variables": {
                "maxDistance": 100000,
                "near": {
                    "cityId": city_id,
                },
                "page": {
                    "first": 16,
                },
                "sortBy": "BEST_FOR_YOU",
            },
        }
    else:
        json_data = {
            "operationName": "ExplorePlacesExploreRadius",
            "query": query_get_places,
            "variables": {
                "maxDistance": 100000,
                "near": {
                    "cityId": city_id,
                },
                "page": {"first": 50, "after": last},
                "sortBy": "BEST_FOR_YOU",
            },
        }

    if AMIGO_BEARER_TOKEN is None:
        raise ValueError("AMIGO_BEARER_TOKEN is not defined.")
    headers = {"Authorization": AMIGO_BEARER_TOKEN}

    try:
        response = requests.post(
            AMIGO_URL + ":" + AMIGO_PORT, json=json_data, headers=headers, timeout=10
        )
    # We catch all exceptions here, because we want to continue the loop
    except Exception as exc:
        print(f"Error: {exc}")
        return None

    # If response.json() is equal to the following, there is no data
    if response.json() == {
        "data": {
            "exploreRadius": {
                "__typename": "ExploreRadius",
                "maxDistance": 40000,
                "recommendedPlaces": {
                    "__typename": "PlacePage",
                    "first": "",
                    "last": "",
                    "items": [],
                },
            }
        }
    }:
        print("No data")
        return None
    data = response.json()

    # Extract only the places we are interested in
    try:
        places = data["data"]["exploreRadius"]["recommendedPlaces"]["items"]

    # TODO: Catch the correct exception
    except Exception as exc:
        print(f"Error: {exc}")
        return None

    if df_places is not None:
        df_places = pd.concat([df_places, pd.json_normalize(places)], ignore_index=True)
    elif df_places is None:
        df_places = pd.json_normalize(places)

    # Extract only the item on the page
    last = data["data"]["exploreRadius"]["recommendedPlaces"]["last"]
    if last == "" or last is None:
        return df_places

    # If there are more items, call the function again
    df_places = get_places(
        name=name, city_id=city_id, region=region, last=last, df_places=df_places
    )
    return df_places
