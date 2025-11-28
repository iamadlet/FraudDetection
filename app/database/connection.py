"""
Database connection and session management
"""

from app.config.settings import DATABASE_URL


class DatabaseConnection:
    """Manages PostgreSQL database connections"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            self.connection = psycopg2.connect(self.connection_string)
            print("✓ Database connection established successfully")
        except ImportError as e:
            print(f"✗ psycopg2 import error: {e}")
            print("Please install: pip install psycopg2-binary")
            raise
        except psycopg2.Error as e:
            print(f"✗ Database connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute a query and return results"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            self.connection.commit()
            results = cursor.fetchall()
            cursor.close()
            return results
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"✗ Query execution failed: {e}")
            raise
    
    def execute_insert(self, query: str, params: tuple = None):
        """Execute an insert query and return the inserted row ID"""
        try:
            import psycopg2
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"✗ Insert execution failed: {e}")
            raise


# Global database connection instance
db = DatabaseConnection(DATABASE_URL)
