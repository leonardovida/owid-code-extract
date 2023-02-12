import os
from pathlib import Path
from typing import List

import pandas as pd
from helpers.amigo.main import extract_amigo, transform_amigo
#from helpers.mapstr.main import extract_mapstr, transform_mapstr


def extract(
    api: List[str],
    df_cities: pd.DataFrame,
):
    """Extract data from all the services provided, one by one.

    TODO: parallel processing of the extraction of data from the different APIs

    Args:
        - api (List[str]): The list of APIs to extract data from.

    """
    res = {}
    for i in api:
        if i == "amigo":
            res[i] = extract_amigo(df_cities)
        # if i == "mapstr":
        #     res[i] = extract_mapstr(df_cities)

    return res


def transform(
    results: dict,
):
    """Extract data from all the services provided, one by one.

    TODO: parallel processing of the extraction of data from the different APIs

    Args:
        - api (List[str]): The list of APIs to extract data from.

    """
    res = {}
    # Iterate over the APIs in api, call each of the transform functions
    # and save the result in the res dictionary to be then aggregated
    dict_df = {}
    for res in results:
        if res == "amigo":
            dict_df[res] = transform_amigo(results[res])
        # if res == "mapstr":
        #     dict_df[res] = transform_mapstr(results[res])

    # From the dictionary of dataframes, aggregate them into one dataframe
    return pd.concat(dict_df.values(), ignore_index=True)


def save(df: pd.DataFrame, output_folder: Path):
    """Save the data into the local output folder.

    Args:
        - output_folder (str): The output folder path in which all the extracted cities will be placed
    Return:
        None: The data is saved in the local output folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    df.to_parquet(os.path.join(output_folder, "data.parquet"))
