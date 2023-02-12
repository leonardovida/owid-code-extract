import pandas as pd
import tqdm

from etl.helpers.amigo.scrape import extract
from etl.helpers.amigo.transform import transform


def extract_amigo(
    df_cities: pd.DataFrame,
):
    """Scrape the amigo API, city by city.

    This function uses an external dataframe, loaded into 'data/input/fixed'
    containing the 15000 biggest cities in the world.

    This dataframe uses the same city ID as the Amigo API and therefore we
    use as a way to retrieve the cities.

    Args:
        df_cities (pd.DataFrame): The dataframe containing the cities to be
    Returns:
        None: Prints the number of cities for which it successfully retrieved
            data from the Amigo API. Also, saves the data in both parquet and xlsx
            format under the
    """
    tqdm.tqdm.pandas(desc="Extracting data from Amigo API")
    df = df_cities.progress_apply(extract, axis=1)

    return df


def transform_amigo(
    df: pd.DataFrame,
):
    """Transform the data retrieved from the amigo API."""
    df = df.progress_apply(transform, axis=1)

    return df
