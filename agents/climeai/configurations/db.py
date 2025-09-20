"""
MongoDB client configuration for the ClimeAI agent.
"""
import os
from pymongo import MongoClient

# Get MongoDB connection string from environment variable or use a default
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")

# Create MongoDB client
mongodb_client = MongoClient(MONGODB_CONNECTION_STRING)
