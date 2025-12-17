# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
# from app.config import settings
# import logging

# logger = logging.getLogger(__name__)

# class MongoDB:
#     def __init__(self):
#         self.client = None
#         self.db = None
#         self._connect()
    
#     def _connect(self):
#         """Establish MongoDB connection"""
#         try:
#             self.client = MongoClient(
#                 settings.MONGO_URI,
#                 serverSelectionTimeoutMS=5000,
#                 connectTimeoutMS=5000
#             )
            
#             # Test connection
#             self.client.admin.command('ping')
#             self.db = self.client[settings.DB_NAME]
            
#             logger.info(f"✅ MongoDB connected to {settings.MONGO_URI}")
            
#         except (ConnectionFailure, ServerSelectionTimeoutError) as e:
#             logger.error(f"❌ MongoDB connection failed: {e}")
#             raise ConnectionError(f"Cannot connect to MongoDB: {e}")
    
#     def get_collection(self, collection_name: str):
#         """Get a collection from database"""
#         if not self.db:
#             raise ConnectionError("Database not connected")
#         return self.db[collection_name]
    
#     def is_connected(self):
#         """Check if database is connected"""
#         try:
#             self.client.admin.command('ping')
#             return True
#         except:
#             return False

# # Global database instance
# db_client = MongoDB()

# # Collection getters
# def get_categories_col():
#     return db_client.get_collection("categories")

# def get_keywords_col():
#     return db_client.get_collection("keywords")

# def get_rules_col():
#     return db_client.get_collection("rules")


from pymongo import MongoClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

def get_categories_col():
    return db.categories

def get_keywords_col():
    return db.keywords

def get_rules_col():
    return db.rules

def get_menus_col():
    return db.menus