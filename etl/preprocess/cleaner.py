import os
from typing import Dict, List


def read_and_clean_file(file_path: str, CITIES_MAPPING, CIRCLE_SIZES) -> List[Dict]:
    """Read and clean single file/list.

    Uses the first entry as city name and appends to each row the word representing
    "restaurant" in the local language.

    Args:
        - file_path (str): The path to the file to read.
        - CITIES_MAPPING (pd.DataFrame): The dataframe containing the mapping between
        - CIRCLE_SIZES (pd.DataFrame): The dataframe containing the mapping between
    Returns:
        - res (List[Dict]): The list of dictionaries containing the cleaned data.
    """
    with open(file_path, encoding="utf-8") as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            print(f"Error on file {file_path}")

        # Use title of the file to get city name, recommnder and optional category
        path, title = os.path.split(file_path)
        title_cleaned = clean_title(title=title)
        city_name = get_city_name(title=title_cleaned)
        recommender = get_recommender(title=title_cleaned)
        list_category = get_list_category(title=title_cleaned)

        # Read list/recommendations
        res = []
        for line in lines[1:]:
            line = clean_line(line=line)
            place, comment = get_comment(line)
            place = clean_place(place)
            if place == "":
                print(f"Empty place found in file {file_path}")
                continue

            # TODO: add the english name if city_name is found
            try:
                row = CITIES_MAPPING.loc[CITIES_MAPPING["city_name"] == city_name]
                if row.shape[0] == 0:
                    row = CITIES_MAPPING.loc[(CITIES_MAPPING["city_english_name"] == city_name)]
                loc_coord = add_coordinates(
                    row["size"].values[0], row["center"].values[0], CIRCLE_SIZES
                )
                loc_rest = row["restaurant_lang"].values[0]
                loc_lang = row["lang"].values[0]
            except IndexError:
                print(f"City not found in mapping \n - {file_path}")
            place = add_localized_restaurant(place, loc_rest)

            # Create dict
            place_dict = {
                "RecommendedPlace": place,
                "RecommendedComment": comment,
                "RecommendedCity": city_name,
                "RecommendedCateogory": list_category,
                "EnrichedLocation": loc_rest,
                "EnrichedCoordinates": loc_coord,
                "EnrichedLanguage": loc_lang,
                "Recommender": recommender,
            }
            res.append(place_dict)
        return res


def get_city_name(title: str) -> str:
    """Get city name.

    Args:
        title (str): The title of the file.

    Returns:
        str: The city name.
    """
    try:
        res = title.split("-")[1].strip()
        return res.split(".txt")[0]
    except:
        print(f"City not found in title {title}")
        raise


def get_recommender(title: str) -> str:
    """Get recommender name.

    Args:
        title (str): The title of the file.

    Returns:
        str: The recommender name.
    """
    try:
        res = title.split("-")[0].strip()
        return res
    except:
        print(f"Recommender name not found in title {title}")
        raise


def get_list_category(title: str) -> str:
    """Get list category.

    Args:
        title (str): The title of the file.

    Returns:
        str: The list category.
    """
    try:
        res = title.split(" - ")[2].strip()
        return res.split(".txt")[0]
    except IndexError:
        return None


def add_coordinates(size, center, CIRCLE_SIZES):
    """Add coordinates.

    Args:
        size (int): The size of the circle.
        center (str): The center of the circle.
        CIRCLE_SIZES (dict): The circle sizes.

    Returns:
        _type_: _description_
    """
    try:
        size_adjustment = CIRCLE_SIZES[size]
        res = "circle:" + str(size_adjustment) + "@" + str(center)
        return res
    except:
        print(f"Error: size {size}, center {center}")


def clean_line(line: str) -> str:
    """Clean line.

    Args:
        line (str): The line to clean.

    Returns:
        str: The cleaned line.
    """
    cleaned_line = line.replace("\n", "").replace(";", "").strip()
    return cleaned_line


def get_comment(line: str) -> str:
    """Get comment from line.

    Args:
        line (str): The line to get the comment from.

    Returns:
        str: The comment.
    """
    for i in ["|", "(", "-", ":"]:
        if i in line[3:]:
            splitted_line = line.split(i)
            comment = splitted_line[1].replace(")", "").replace("-", "").strip()
            place = splitted_line[0]
            return (place, comment)
    return (line, None)


def add_localized_restaurant(line: str, localized_restaurant) -> str:
    """Add localized restaurant to line.

    Args:
        line (str): The line to add the localized restaurant to.
        localized_restaurant (str): The localized restaurant.

    Returns:
        str: The line with the localized restaurant added.
    """
    for i in ["café", "bar"]:
        if i in line.lower():
            return line
    return line + f" {localized_restaurant}"


def clean_place(place: str) -> str:
    """Clean place name.

    Args:
        place (str): The place name to clean.

    Returns:
        str: The cleaned place name.
    """
    res = place.strip().replace("-", "").strip()
    return res


def clean_title(title: str) -> str:
    """Clean title.

    Args:
        title (str): The title to clean.

    Returns:
        str: The cleaned title.
    """
    res = title.strip().replace(";", "").replace(":", "").lower()
    return res
