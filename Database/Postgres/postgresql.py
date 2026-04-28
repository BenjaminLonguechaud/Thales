"""
PostgreSQL Database Connection and CRUD Operations Module
Connects to PostgreSQL deployed in Kubernetes and provides table interaction.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool, Error
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PostgreSQLDatabase:
    """
    PostgreSQL database connection manager with connection pooling.
    Handles CRUD operations and provides utilities for database interaction.
    """

    def __init__(
        self,
        host: str,
        port: int = 5432,
        database: str = "postgres",
        user: str = "postgres",
        password: str = "postgres",
        min_connections: int = 2,
        max_connections: int = 10,
    ):
        """
        Initialize the database connection pool.

        Args:
            host: PostgreSQL server hostname or IP address
            port: PostgreSQL server port (default: 5432)
            database: Database name
            user: Database user
            password: Database password
            min_connections: Minimum connections in pool
            max_connections: Maximum connections in pool
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.connection_pool = None

        try:
            self._create_connection_pool()
            logger.info(f"Successfully connected to PostgreSQL at {host}:{port}")
        except Error as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def _create_connection_pool(self):
        """Create a connection pool for efficient database access."""
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            self.min_connections,
            self.max_connections,
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        logger.info("Connection pool created successfully")

    @contextmanager
    def get_connection(self):
        """Context manager to get a connection from the pool."""
        connection = self.connection_pool.getconn()
        try:
            yield connection
            connection.commit()
        except Error as e:
            connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            self.connection_pool.putconn(connection)

    def close_all_connections(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("All connections closed")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.

        Args:
            query: SQL query string
            params: Query parameters (optional)

        Returns:
            List of dictionaries containing query results
        """
        with self.get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string
            params: Query parameters (optional)

        Returns:
            Number of rows affected
        """
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount

    def create_table(self, table_name: str, schema: Dict[str, str]) -> bool:
        """
        Create a table with the specified schema.

        Args:
            table_name: Name of the table to create
            schema: Dictionary mapping column names to PostgreSQL data types
                   Example: {"id": "SERIAL PRIMARY KEY", "name": "VARCHAR(255)"}

        Returns:
            True if successful, False otherwise
        """
        try:
            columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"

            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)

            logger.info(f"Table '{table_name}' created successfully")
            return True
        except Error as e:
            logger.error(f"Error creating table: {e}")
            return False

    def insert_record(self, table_name: str, record: Dict[str, Any]) -> bool:
        """
        Insert a single record into the table.

        Args:
            table_name: Name of the table
            record: Dictionary with column names as keys and values to insert

        Returns:
            True if successful, False otherwise
        """
        try:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["%s"] * len(record))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            self.execute_update(query, tuple(record.values()))
            logger.info(f"Record inserted into '{table_name}'")
            return True
        except Error as e:
            logger.error(f"Error inserting record: {e}")
            return False

    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> int:
        """
        Insert multiple records into the table.

        Args:
            table_name: Name of the table
            records: List of dictionaries to insert

        Returns:
            Number of records inserted
        """
        if not records:
            return 0

        try:
            count = 0
            for record in records:
                if self.insert_record(table_name, record):
                    count += 1
            return count
        except Error as e:
            logger.error(f"Error inserting records: {e}")
            return 0

    def select_all(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Select all records from a table.

        Args:
            table_name: Name of the table

        Returns:
            List of dictionaries containing all records
        """
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)

    def select_by_condition(
        self, table_name: str, condition: str, params: tuple = None
    ) -> List[Dict[str, Any]]:
        """
        Select records matching a condition.

        Args:
            table_name: Name of the table
            condition: WHERE clause condition (e.g., "id = %s")
            params: Parameters for the condition

        Returns:
            List of dictionaries matching the condition
        """
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return self.execute_query(query, params)

    def update_record(
        self, table_name: str, updates: Dict[str, Any], condition: str, params: tuple = None
    ) -> int:
        """
        Update records matching a condition.

        Args:
            table_name: Name of the table
            updates: Dictionary of column names and new values
            condition: WHERE clause condition
            params: Parameters for the condition

        Returns:
            Number of rows updated
        """
        set_clause = ", ".join([f"{col} = %s" for col in updates.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

        all_params = tuple(updates.values()) + (params or ())
        return self.execute_update(query, all_params)

    def delete_records(self, table_name: str, condition: str, params: tuple = None) -> int:
        """
        Delete records matching a condition.

        Args:
            table_name: Name of the table
            condition: WHERE clause condition
            params: Parameters for the condition

        Returns:
            Number of rows deleted
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        return self.execute_update(query, params)

    def drop_table(self, table_name: str) -> bool:
        """
        Drop a table from the database.

        Args:
            table_name: Name of the table to drop

        Returns:
            True if successful, False otherwise
        """
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
            logger.info(f"Table '{table_name}' dropped successfully")
            return True
        except Error as e:
            logger.error(f"Error dropping table: {e}")
            return False

    def execute_raw_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Execute a raw SQL query with full control.

        Args:
            query: Raw SQL query string
            params: Query parameters (optional)

        Returns:
            Query results as list of dictionaries
        """
        return self.execute_query(query, params)

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about table columns.

        Args:
            table_name: Name of the table

        Returns:
            List of dictionaries containing column information
        """
        query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        return self.execute_query(query, (table_name,))


def get_database_from_env() -> PostgreSQLDatabase:
    """
    Create a database connection using environment variables.

    Expected environment variables:
    - DB_HOST: PostgreSQL host
    - DB_PORT: PostgreSQL port (default: 5432)
    - DB_NAME: Database name (default: postgres)
    - DB_USER: Database user (default: postgres)
    - DB_PASSWORD: Database password (default: postgres)

    Returns:
        PostgreSQLDatabase instance
    """
    return PostgreSQLDatabase(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


if __name__ == "__main__":
    # Example usage
    print("PostgreSQL Database Module loaded successfully")
