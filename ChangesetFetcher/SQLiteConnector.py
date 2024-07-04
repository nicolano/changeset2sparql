import sqlite3
import logging

from Changeset import Changeset
from time import strftime

TABLE_NAME_CHANGESETS = 'changesets'
SQL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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
        table_definition = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_CHANGESETS}(
    id INTEGER PRIMARY KEY,
    created_at DATETIME,
    closed_at DATETIME,
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
        logging.info("Table created successfully")

    def insert_changeset(self, changeset: Changeset):
        """
        Inserts a changeset into the database. If a changeset with the given id already exists, it will be ignored.
        :return:
        """
        created_at = changeset.created_at.strftime(SQL_TIME_FORMAT)
        if changeset.closed_at is None:
            closet_at: str = ""
        else:
            closet_at: str = changeset.closed_at.strftime(SQL_TIME_FORMAT) or None

        self.__cursor.execute(
            f"""INSERT OR IGNORE  INTO {TABLE_NAME_CHANGESETS} VALUES (
            {changeset.id},
            \'{created_at}\',
            \'{closet_at}\',
            \'{changeset.user}\',
            {changeset.uid},
            {changeset.min_lat},
            {changeset.min_lon},
            {changeset.max_lat},
            {changeset.max_lon},
            {changeset.comments_count},
            {changeset.num_changes}
            );
            """
        )
        self.__connection.commit()
        logging.info(
            f"""Either Inserted changeset with id {changeset.id} into table {TABLE_NAME_CHANGESETS} or there 
                already exists changeset with id {changeset.id}
            """
        )
