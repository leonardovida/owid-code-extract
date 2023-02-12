"""
    Command line interface for the ETL pipeline.
"""
from pathlib import Path
from typing import List

import click

from etl.helpers.common.utils import filter_cities
from etl.utils import extract, save, transform


@click.command()
@click.option(
    "--api",
    "-a",
    multiple=True,
    default=["amigo"],
    type=click.Choice(["amigo", "mapstr"]),
    is_flag=False,
    help="The API to be used for extracting data from. This can be one or more of the following "
    "values: 'amigo', 'mapstr'",
)
@click.option(
    "--city-population",
    "-c",
    default=300000,
    is_flag=False,
    help=(
        "The lower threshold of population on which to filter a list of the top 15000 cities by "
        "population and query the selected API with. The default value is 300000."
    ),
)
@click.option(
    "--geo-area",
    "-g",
    is_flag=False,
    multiple=True,
    default=["europe", "america", "australia", "asia"],
    type=click.Choice(["europe", "america", "australia", "asia"]),
    help="The geographical area for which available cities will be extracted. This can one or more "
    'of the following values: "europe", "america", "australia", "asia"',
)
@click.option(
    "--output-folder",
    "-o",
    is_flag=False,
    type=click.Path(exists=True),
    default="data/output/amigo",
    help="The output folder path in which all the extracted cities will be placed",
)
@click.option(
    "--save-local",
    "-s",
    is_flag=True,
    help="Save the data in the local output folder",
    default=False,
)
def main_cli(
    api: List[str],
    city_population: int,
    geo_area: List[str],
    output_folder: str,
    save_local: bool,
) -> None:
    """Scrape the selected API, city by city.

    Args:
        - city_population (int): The lower threshold of population on which to
            filter a list of the top 15000 cities by population and query the API
        - geoarea (str): The geographical area for which available cities
            will be extracted. This can one or more of the following values: 'Europe', 'America',
            'Australia', 'Asia'
        - output_folder (str): The output folder path in which all the extracted cities
            will be placed

    Returns:
        None: Prints the number of cities for which it successfully retrieved
    """
    kwargs = dict(
        api=api,
        city_population=city_population,
        geo_area=geo_area,
        output_folder=output_folder,
        save_local=save_local,
    )
    main(**kwargs)


def main(
    api: List[str],
    city_population: int,
    geo_area: List[str],
    output_folder: Path,
    save_local: bool,
) -> None:
    """Scrape the selected API, city by city.

    This function uses an external dataframe, loaded into 'data/input/fixed'
    containing the 15000 biggest cities in the world.

    Args:
        city_pop_size (int): The lower threshold of population on which to
            filter a list of the top 15000 cities by population and query
            the Amingo API with.
        geographical_area (str): The geographical area for which available cities
            will be extracted. This can one or more of the following values: 'Europe', 'America',
            'Australia', 'Asia'
        output_folder (str): The output folder path in which all the extracted cities will be placed
        application_token (str, Optional):
        uuid (str, Optional):
    Returns:
        None: Prints the number of cities for which it successfully retrieved
            data from the Amigo API. Also, saves the data in both parquet and xlsx
            format under the
    """
    df_cities = None
    try:
        # Select cities
        df_cities = filter_cities(geographical_area=geo_area, population_threshold=city_population)

        # Extract data from amigo using selected cities
        df = extract(df_cities=df_cities, api=api)

        # Clean and transform extracted data to common structure
        df = transform(results=df)

        # Load to database and export
        # load(df=df) commented out for OWID application

        # If selected, save local ouput to check data in parquet format
        if save_local:
            save(df=df, output_folder=output_folder)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if df_cities is not None:
            print(f"Retrieved data from {len(df_cities)} cities.")


if __name__ == "__main__":
    main_cli()
