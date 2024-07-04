import logging
import datetime

from xml.etree.ElementTree import Element
from typing import Optional

from Changeset import Changeset

KEY_ID = "id"
KEY_CREATED_AT = "created_at"
KEY_CLOSED_AT = "closed_at"
KEY_OPEN = "open"
KEY_USER = "user"
KEY_UID = "uid"
KEY_MIN_LAT = "min_lat"
KEY_MIN_LOT = "min_lon"
KEY_MAX_LAT = "max_lat"
KEY_MAX_LON = "max_lon"
KEY_COMMENTS_COUNT = "comments_count"
KEY_NUM_CHANGES = "num_changes"


def map_element_to_changeset(element: Element) -> Changeset:
    """
    Maps an XML element that represents a changeset to a changeset object.
    :param element:
    :return:
    """
    return Changeset(
        id=int(get_value_from_element_attribute(element, KEY_ID)),
        created_at=get_date_time_from_string(get_value_from_element_attribute(element, KEY_CREATED_AT)),
        closed_at=get_date_time_from_string(get_value_from_element_attribute(element, KEY_CLOSED_AT)),
        open=bool(get_value_from_element_attribute(element, KEY_OPEN)),
        user=get_value_from_element_attribute(element, KEY_USER),
        uid=int(get_value_from_element_attribute(element, KEY_UID)),
        min_lat=float(get_value_from_element_attribute(element, KEY_MIN_LAT)),
        min_lon=float(get_value_from_element_attribute(element, KEY_MIN_LOT)),
        max_lat=float(get_value_from_element_attribute(element, KEY_MAX_LAT)),
        max_lon=float(get_value_from_element_attribute(element, KEY_MAX_LON)),
        comments_count=int(get_value_from_element_attribute(element, KEY_COMMENTS_COUNT)),
        num_changes=int(get_value_from_element_attribute(element, KEY_NUM_CHANGES)),
    )


def get_value_from_element_attribute(element: Element, key: str) -> Optional[str]:
    try:
        return element.attrib[key]
    except KeyError:
        logging.warning(f"Could not find attribute with key: {key}")
        return None


def get_date_time_from_string(date_time_string: str) -> Optional[datetime.datetime]:
    if date_time_string is None:
        return None
    else:
        return datetime.datetime.strptime(date_time_string, "%Y-%m-%dT%H:%M:%S%z")
