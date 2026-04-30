# backend/utils/db_utils.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

load_dotenv()

class Database:
    """Handles MongoDB client connection and testing."""
    
    def __init__(self):
        # Read environment variable
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI environment variable not set.")
        
        # Initialize client
        self.client = MongoClient(uri)
        # self.db_name = os.getenv("MONGO_DB_NAME", "plantoship")

    async def test_connection(self):
        """Performs a ping test to verify live connection status."""
        try:
            self.client.admin.command("ping")
            return True, "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            return False, f"{e}"

# Usage elsewhere (Startup hook):
# db = Database()
# success, message = await db.test_connection()
