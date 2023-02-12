"""This module contains the GraphQL queries used to extract data from Amigo.

The queries might be broken at any time as the API evolves. If that happens,
use the notebook in the notebooks/amigo folder using https://mitmproxy.org/
to record the queries and update this file accordingly.
"""

query_get_places = """
    query
    ExplorePlacesExploreRadius($near: ExploreNear!, $maxDistance: Int, $categoryId: String, $filter: PlacesFilter, $sortBy: PlacesSortBy!, $page: PageRequest)
        {
            exploreRadius(near: $near, maxDistance: $maxDistance)
                {
                    maxDistance
                    recommendedPlaces(filter: $filter, sortBy: $sortBy, page: $page)
                    {
                        first
                        last
                        items {
                            ...ExplorePlacesPlace
                        }
                    }
                }
            }
            fragment ExplorePlacesPlace on Place
                {
                    id
                    name
                    permalink
                    mustGoByYou(category: $categoryId)
                    recommendedByYou(category: $categoryId)
                    isTrending
                    details {
                        ...PlaceInformation
                    }
                    city {
                        id
                        name
                        stateCode
                        country {
                            id
                            name
                        }
                    }
                    attributes {
                        ...PlaceAttributeDetails
                    }
                    categories {
                        ...PlaceCategoryDetails
                    }
                    coordinates {
                        lat
                        lng
                    }
                    visitedCount {
                        amigos
                        others
                        guides
                        total
                    }
                    mustGoCount {
                        amigos
                        others
                        guides
                        total
                    }
                    wannaGoCount {
                        amigos
                        others
                        guides
                        total
                    }
                    typesData {
                        ...PlaceTypeDetails
                    }
                    notes {
                        items {
                            ...BaseNoteDetails
                        }
                    }
                    guidePicks {
                        mustGo
                        tip {
                            ...NoteText
                        }
                    }
                }
                fragment PlaceTypeDetails on PlaceType {
                    name
                }
                fragment PlaceAttributeDetails on PlaceAttribute {
                    name
                    values {
                        ...PlaceAttributeValueDetails
                    }
                }
                fragment PlaceAttributeValueDetails on PlaceAttributeValue {
                    name
                }
                fragment PlaceInformation on PlaceDetails {
                    address
                    pageUrl
                    costRate
                    contact {
                        phone
                    }
                    menu {
                        label
                        url
                    }
                    openingHours {
                        ...OpeningHoursDetails
                    }
                }
                fragment OpeningHoursDetails on OpeningHours {
                    days
                    open
                }
                fragment PlaceCategoryDetails on PlaceCategory {
                    name
                    primary
                }
                fragment NoteText on Note {
                    id
                    text
                }
                fragment BaseNoteDetails on Note {
                    text
                }
                """
