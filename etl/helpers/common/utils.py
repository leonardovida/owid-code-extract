import os
from typing import List

import pandas as pd

from etl.config import AMIGO_PORT, AMIGO_URL
from etl.paths import FIXED_INPUT_DIR

# Url for the Amigo API
URL_AMIGO = AMIGO_URL + ":" + AMIGO_PORT


def filter_cities(geographical_area: List[str], population_threshold: int):
    """Filter the cities dataframe to scrape the Amigo API

    Args:
        geographical_area (List[str]): The geographical area
            for which we are interested in retrieving the cities
        population_threshold (int): The minimum population threshold
            for which we are intereted in retrieving the cities

    Returns:
        pd.DataFrame: The filtered cities dataframe
    """
    # Read txt data file with cities in a dataframe using tab as delimiter
    df = pd.read_csv(os.path.join(FIXED_INPUT_DIR, "cities15000.txt"), sep="\t", header=None)

    # Reverse order by column 14 (population)
    df = df.sort_values(by=[14], ascending=False)

    # Column 17 represents the region but can be of different types
    # e.g. Europe/Berlin, Europe/Amsterdam, etc.
    # Filter df on the selected area
    for area in geographical_area:
        df = df[df[17].str.lower().str.startswith(str.lower(area))]

    # Filter df on the population threshold
    return (
        df.loc[df[14] >= population_threshold]
      .rename(columns={0: "id", 2: "city_name", 14: "population", 17: "region"})
)