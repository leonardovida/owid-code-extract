import time

import pandas as pd


def find_places(row: str, gmaps):
    """Main enrich function calling google maps"""
    time.sleep(0.1)
    res = gmaps.find_place(
        input=row["RecommendedPlace"],
        fields=[
            "business_status",
            "formatted_address",
            "name",
            "plus_code",
            "price_level",
            "rating",
            "types",
            "user_ratings_total",
            "permanently_closed",
        ],  # last three more expensive
        input_type="textquery",
        location_bias=row["EnrichedCoordinates"],
        language=row["EnrichedLanguage"],
    )
    try:
        return pd.Series(
            [
                res.get("candidates")[0].get("business_status"),
                res.get("candidates")[0].get("formatted_address"),
                res.get("candidates")[0].get("name"),
                res.get("candidates")[0].get("plus_code").get("global_code"),
                res.get("candidates")[0].get("price_level"),
                res.get("candidates")[0].get("rating"),
                res.get("candidates")[0].get("types"),
                res.get("candidates")[0].get("user_ratings_total"),
                res.get("status"),
            ]
        )
    except:
        print(f'{row["RecommendedPlace"]} was not found')
        return pd.Series(
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ]
        )


## Utils

import warnings

from googlemaps import convert

PLACES_FIND_FIELDS_BASIC = {
    "business_status",
    "formatted_address",
    "geometry",
    "geometry/location",
    "geometry/location/lat",
    "geometry/location/lng",
    "geometry/viewport",
    "geometry/viewport/northeast",
    "geometry/viewport/northeast/lat",
    "geometry/viewport/northeast/lng",
    "geometry/viewport/southwest",
    "geometry/viewport/southwest/lat",
    "geometry/viewport/southwest/lng",
    "icon",
    "name",
    "permanently_closed",
    "photos",
    "place_id",
    "plus_code",
    "types",
}

PLACES_FIND_FIELDS_CONTACT = {"opening_hours"}

PLACES_FIND_FIELDS_ATMOSPHERE = {"price_level", "rating", "user_ratings_total"}

PLACES_FIND_FIELDS = (
    PLACES_FIND_FIELDS_BASIC ^ PLACES_FIND_FIELDS_CONTACT ^ PLACES_FIND_FIELDS_ATMOSPHERE
)

PLACES_DETAIL_FIELDS_BASIC = {
    "address_component",
    "adr_address",
    "business_status",
    "formatted_address",
    "geometry",
    "geometry/location",
    "geometry/location/lat",
    "geometry/location/lng",
    "geometry/viewport",
    "geometry/viewport/northeast",
    "geometry/viewport/northeast/lat",
    "geometry/viewport/northeast/lng",
    "geometry/viewport/southwest",
    "geometry/viewport/southwest/lat",
    "geometry/viewport/southwest/lng",
    "icon",
    "name",
    "permanently_closed",
    "photo",
    "place_id",
    "plus_code",
    "type",
    "url",
    "utc_offset",
    "vicinity",
}

PLACES_DETAIL_FIELDS_CONTACT = {
    "formatted_phone_number",
    "international_phone_number",
    "opening_hours",
    "website",
}

PLACES_DETAIL_FIELDS_ATMOSPHERE = {"price_level", "rating", "review", "user_ratings_total"}

PLACES_DETAIL_FIELDS = (
    PLACES_DETAIL_FIELDS_BASIC ^ PLACES_DETAIL_FIELDS_CONTACT ^ PLACES_DETAIL_FIELDS_ATMOSPHERE
)

DEPRECATED_FIELDS = {"permanently_closed"}
DEPRECATED_FIELDS_MESSAGE = (
    "Fields, %s, are deprecated. " "Read more at https://developers.google.com/maps/deprecations."
)


def _find_place_request(client, input, input_type, fields=None, location_bias=None, language=None):
    """
    A Find Place request takes a text input, and returns a place.
    The text input can be any kind of Places data, for example,
    a name, address, or phone number.
    :param input: The text input specifying which place to search for (for
                  example, a name, address, or phone number).
    :type input: string
    :param input_type: The type of input. This can be one of either 'textquery'
                  or 'phonenumber'.
    :type input_type: string
    :param fields: The fields specifying the types of place data to return. For full details see:
                   https://developers.google.com/places/web-service/search#FindPlaceRequests
    :type fields: list
    :param location_bias: Prefer results in a specified area, by specifying
                          either a radius plus lat/lng, or two lat/lng pairs
                          representing the points of a rectangle. See:
                          https://developers.google.com/places/web-service/search#FindPlaceRequests
    :type location_bias: string
    :param language: The language in which to return results.
    :type language: string
    :rtype: result dict with the following keys:
            status: status code
            candidates: list of places
    """
    params = {"input": input, "inputtype": input_type}

    if input_type != "textquery" and input_type != "phonenumber":
        raise ValueError(
            "Valid values for the `input_type` param for "
            "`find_place` are 'textquery' or 'phonenumber', "
            f"the given value is invalid: '{input_type}'"
        )

    if fields:
        deprecated_fields = set(fields) & DEPRECATED_FIELDS
        if deprecated_fields:
            warnings.warn(
                DEPRECATED_FIELDS_MESSAGE % str(list(deprecated_fields)),
                DeprecationWarning,
            )

        invalid_fields = set(fields) - PLACES_FIND_FIELDS
        if invalid_fields:
            raise ValueError(
                "Valid values for the `fields` param for "
                "`find_place` are '%s', these given field(s) "
                "are invalid: '%s'" % ("', '".join(PLACES_FIND_FIELDS), "', '".join(invalid_fields))
            )
        params["fields"] = convert.join_list(",", fields)

    if location_bias:
        valid = ["ipbias", "point", "circle", "rectangle"]
        if location_bias.split(":")[0] not in valid:
            raise ValueError("location_bias should be prefixed with one of: %s" % valid)
        params["locationbias"] = location_bias
    if language:
        params["language"] = language

    return client._request("/maps/api/place/findplacefromtext/json", params)
