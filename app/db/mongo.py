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