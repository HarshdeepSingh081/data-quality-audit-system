"""
Data extraction module for connecting to MySQL database
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from config.database_config import db_config

class DataExtractor:
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host = db_config["host"],
                user = db_config["user"],
                password = db_config["password"],
                database = db_config["database"]
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        try:
            df = pd.read_sql(query, self.connection)
            return df
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_table_data(self, table_name):
        """Fetch all data from a specific table"""
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")