import urllib.request
import gzip
import xml.etree.ElementTree as eT

from XmlElementToChangeset import map_element_to_changeset
from SQLiteConnector import (SQLiteConnector)
from Changeset import Changeset

BASE_URL = "https://planet.openstreetmap.org/replication/changesets/"
DATABASE_NAME = "changesets.db"


class ChangesetFetcher:
    sqlConnector: SQLiteConnector

    """
    Fetches the Changsets from the osm server and stores them in a sql database.
    """

    def __init__(self):
        self.sqlConnector = SQLiteConnector(DATABASE_NAME)
        print()

    def urlBuilder(self, date: str) -> str:
        return 'https://planet.openstreetmap.org/replication/changesets/006/079/372.osm.gz'

    def fetch_changesets(self):
        with urllib.request.urlopen(self.urlBuilder("")) as f:
            f = gzip.open(f, 'rb')
            html = f.read().decode('utf-8')
            root = eT.fromstring(html)

            changesets: list[Changeset] = []
            for child in root:
                changesets.append(map_element_to_changeset(child))

            print(len(changesets))

            for changeset in changesets:
                self.sqlConnector.insert_changeset(changeset)


def main() -> None:
    cf = ChangesetFetcher()
    cf.fetch_changesets()


if __name__ == "__main__":
    main()
