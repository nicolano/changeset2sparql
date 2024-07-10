import logging
import urllib.request
import gzip
import xml.etree.ElementTree as eT
from datetime import datetime
import Constants
from typing import Optional
import HtmlHelper
import pytz

from XmlElementToChangeset import map_element_to_changeset
from SQLiteConnector import (SQLiteConnector)
from Changeset import Changeset

BASE_URL = "https://planet.openstreetmap.org/replication/changesets"
DATABASE_NAME = "changesets.db"
OSM_CHANGESET_API_URL = "https://www.openstreetmap.org/api/0.6/changeset/"
OSM_CHANGESETS_API_URL = "https://www.openstreetmap.org/api/0.6/changesets/"
MAX_FETCH_SIZE = 100

class ChangesetFetcher:
    sqlConnector: SQLiteConnector

    """
    Fetches the Changesets from the osm server and stores them in a sql database.
    """

    def __init__(self):
        self.sqlConnector = SQLiteConnector(DATABASE_NAME)

    def fetch_changesets(self, from_date: datetime, to_date: Optional[datetime] = None):
        """
        Returns a list of all changesets between from_date and to_date.

        Uses the ``/api/0.6/changesets`` backend (see
        https://wiki.openstreetmap.org/wiki/API_v0.6#Query:_GET_/api/0.6/changesets)

        :param from_date: The date from which to start fetching changesets.
        :param to_date: The date up to which the changesets should be fetched. Default is now.
        :return: The list of changesets between from_date and to_date.
        """
        changesets: list[Changeset] = []

        logging.info(f"Start fetch from date {from_date}")
        fetch_incomplete = True
        while fetch_incomplete:
            time_param: str = "?time="
            if to_date is None:
                time_param += from_date.strftime(Constants.OSM_DATETIME_FORMAT)
            else:
                time_param += (from_date.strftime(Constants.OSM_DATETIME_FORMAT)
                               + to_date.strftime(Constants.OSM_DATETIME_FORMAT))

            url = OSM_CHANGESETS_API_URL + time_param + "&closed=true"
            changeset_batch: list[Changeset] = []
            with urllib.request.urlopen(url) as f:
                root = eT.fromstring(f.read().decode('utf-8'))
                for child in root:
                    changeset_batch.append(map_element_to_changeset(child))

            changesets.extend(changeset_batch)

            # The osm server returns at most MAX_FETCH_SIZE elements, so we have to check if there are more changesets
            # to fetch
            if len(changeset_batch) == MAX_FETCH_SIZE:
                from_date = changeset_batch[0].closed_at
                logging.info(f"Fetch incomplete: start new fetch from date {from_date}")
            else:
                fetch_incomplete = False

            changeset_batch.clear()

        if to_date is None:
            logging.info(f"Fetched {len(changesets)} changesets from {from_date} to {datetime.now()}")
        else:
            logging.info(f"Fetched {len(changesets)} changesets from {from_date} to {to_date}")

        for changeset in changesets:
            self.sqlConnector.insert_changeset(changeset)

    @staticmethod
    def get_data_for_changeset(changeset: Changeset):
        url: str = OSM_CHANGESET_API_URL + str(changeset.id) + "/download"
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            root = eT.fromstring(html)
            print(html)
            to_modify: [eT.Element] = []
            for modify in root:
                if modify.tag == "modify":
                    for element in modify:
                        to_modify.append(element)

            to_insert: [eT.Element] = []
            for create in root:
                if create.tag == "create":
                    for element in create:
                        to_insert.append(element)

            to_delete: [eT.Element] = []
            for create in root:
                if create.tag == "delete":
                    for element in create:
                        to_delete.append(element)

            print(to_modify)

            f = open("tmp.txt", "w")
            for element in to_modify:
                f.write(eT.tostring(element, encoding="unicode"))
            f.close()

            print(to_insert)
            print(to_delete)


def main() -> None:
    logging.getLogger().setLevel(logging.INFO)
    cf = ChangesetFetcher()
    date = pytz.UTC.localize(datetime(2024, 7, 10, 10, 25))
    cf.fetch_changesets(
        from_date=date
    )
    # print(changesets[0])
    # data = cf.get_data_for_changeset(changesets[0])


if __name__ == "__main__":
    main()
