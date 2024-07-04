import sqlite3
import logging

from Changeset import Changeset


class SQLiteConnector:
    """
    A Database connector for a sqlite database.
    """
    __connection: sqlite3.Connection = None
    __cursor: sqlite3.Cursor = None
    databaseName: str = None

    def __init__(self, database_name: str):
        """
        Creates a connector to the database with the passed name.

        :param database_name: Name of the database file
        """
        self.databaseName = database_name
        self.__connect_to_database()
        self.__create_table_for_changesets()

    def __connect_to_database(self):
        """
        Connect to the sqlite database
        :return:
        """
        try:
            self.__connection = sqlite3.connect(self.databaseName)
            self.__cursor = self.__connection.cursor()
            logging.info("Connected to database")
        except:
            logging.error(f'Could not connect to database {self.databaseName}')

    def __create_table_for_changesets(self):
        """
        Creates the table to store the changesets if this table does not already exist in the database.
        :return:
        """
        table_definition = """CREATE TABLE IF NOT EXISTS changesets(
    id INTEGER PRIMARY KEY,
    created_at DATE,
    closed_at DATE,
    user TEXT,
    user_id INTEGER,
    min_lat REAL,
    min_lon REAL,
    max_lat REAL,
    max_lon REAL,
    comments_count INTEGER,
    changes_count INTEGER
);"""
        self.__cursor.execute(table_definition)

    def insert_changeset(self, changeset: Changeset):
        """
        Inserts a changeset into the database
        :return:
        """
        self.__cursor.execute(
            f"INSERT INTO {self.databaseName} VALUES ({changeset.id},{changeset.created_at},{changeset.closed_at},{changeset.user},{changeset.user_id},{changeset.min_lat},{changeset.min_lon},{changeset.max_lat},{changeset.max_lon},{changeset.comments_count},{changeset.changes_count})"
        )
        self.__connection.commit()
