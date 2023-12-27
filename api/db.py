import mysql.connector
from decouple import config as env

from api.logger import logger
from api.exceptions import DBConnectionError
from api.utils import is_iterable


class DB:
    def __init__(self, config=env):
        """
        Initialize the DB class.

        Parameters:
        - config (callable): Decouple configuration function (Optional).
        """
        self._config = self._load_config()
        self._initialize_tables()

    def _load_config(self):
        """
        Load database configuration from environment variables.

        Returns:
        dict: Database configuration.
        """
        config = {
            "user": env("SQL_USER"),
            "password": env("SQL_PASSWORD"),
            "host": env("SQL_HOST"),
            "database": env("SQL_DB"),
            "port": env("SQL_PORT", 3306),
        }

        try:
            config["port"] = int(config["port"])
        except ValueError:
            logger.warning(
                "Port provided in .env is not int-parsable. Defaulting to port 3306"
            )
            config["port"] = 3306

        return config

    def _connect(self) -> mysql.connector.CMySQLConnection:
        """
        Establish a connection to the database.
        """
        try:
            connection = mysql.connector.connect(**self._config)
        except (
            mysql.connector.InterfaceError,
            mysql.connector.ProgrammingError,
        ) as err:
            logger.critical(f"Failed to connect to DB: {err}")
            raise DBConnectionError(
                message=f"Unable to connect to the database. \n{err}"
            )
        return connection

    def _initialize_tables(self):
        """
        Initialize database tables if they don't exist.
        """
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS cards (
                owner_username VARCHAR(255) PRIMARY KEY,
                balance INT
            );"""
        )

    def execute_queries(self, query, values):
        """
        Execute a list of SQL queries.

        Parameters:
        - query (str): SQL query string.
        - values (list(tuple)): List of values to be substituted into the query.

        Returns:
        - Results of all of the queries.
        """
        logger.debug(
            f"Executing a MySQL query list:\nQuery: {query}\nValues Pool: {values}"
        )
        connection = self._connect()
        cursor = connection.cursor()
        try:
            cursor.executemany(query, values)
            result = cursor.fetchall()
            connection.commit()
            return result
        except mysql.connector.Error as err:
            logger.error(
                f"MySQL error during a query:\nQuery: {query}\nValues: {values}\nError: {err}"
            )
            connection.rollback()
            return False

    def execute_query(self, query, values=None):
        """
        Execute a SQL query.

        Parameters:
        - query (str): SQL query string.
        - values (tuple): Values to be substituted into the query.

        Returns:
        - Results of the query.
        """
        logger.debug(f"Executing a MySQL query:\nQuery: {query}\nValues: {values}")

        connection = self._connect()
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            connection.commit()
            if len(result) == 1 and is_iterable(result):
                result = result[0]
            return result
        except mysql.connector.Error as err:
            logger.error(
                f"MySQL error during a query:\nQuery: {query}\nValues: {values}\nError: {err}"
            )
            connection.rollback()
            return False
