import os

def get_db():
    """Connect to MongoDB container with fallback"""
    try:
        from pymongo import MongoClient
        uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
        client = MongoClient(uri)
        return client[os.getenv("MONGO_DB", "appstarai_db")]
    except Exception as e:
        # Return a mock database object that won't crash the app
        class MockDB:
            def insert_one(self, *args, **kwargs):
                pass  # Silently fail for testing
        
        class MockClient:
            def __getitem__(self, name):
                return MockDB()
        
        return MockDB()

