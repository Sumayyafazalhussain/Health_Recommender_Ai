
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from app.db.mongo import get_categories_col, get_keywords_col, get_rules_col

# def seed_database():
#     """Seed the database with initial data"""
#     print("🌱 Seeding database with initial data...")
    
#     # Clear existing data
#     get_categories_col().delete_many({})
#     get_keywords_col().delete_many({})
#     get_rules_col().delete_many({})
    
#     # Insert categories
#     categories = [
#         {
#             "_id": "fast_food",
#             "name": "Fast Food",
#             "description": "Fast food restaurants",
#             "is_unhealthy": True
#         },
#         {
#             "_id": "bar",
#             "name": "Bar/Pub",
#             "description": "Bars and pubs",
#             "is_unhealthy": True
#         },
#         {
#             "_id": "gym",
#             "name": "Gym",
#             "description": "Gyms and fitness centers",
#             "is_unhealthy": False
#         },
#         {
#             "_id": "smoothie",
#             "name": "Smoothie Shop",
#             "description": "Healthy smoothie and juice bars",
#             "is_unhealthy": False
#         },
#         {
#             "_id": "walking_trail",
#             "name": "Walking Trail",
#             "description": "Walking paths and trails",
#             "is_unhealthy": False
#         },
#         {
#             "_id": "healthy_cafe",
#             "name": "Healthy Cafe",
#             "description": "Healthy cafes and restaurants",
#             "is_unhealthy": False
#         }
#     ]
    
#     get_categories_col().insert_many(categories)
#     print(f"✅ Added {len(categories)} categories")
    
#     # Insert keywords
#     keywords = [
#         # Fast food keywords
#         {"keyword": "mcdonald", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "mcdonald's", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "burger king", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "kfc", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "subway", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "pizza hut", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "taco bell", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "wendy's", "category_id": "fast_food", "match_type": "partial"},
#         {"keyword": "domino's", "category_id": "fast_food", "match_type": "partial"},
        
#         # Bar keywords
#         {"keyword": "bar", "category_id": "bar", "match_type": "partial"},
#         {"keyword": "pub", "category_id": "bar", "match_type": "partial"},
#         {"keyword": "tavern", "category_id": "bar", "match_type": "partial"},
#         {"keyword": "lounge", "category_id": "bar", "match_type": "partial"},
#         {"keyword": "nightclub", "category_id": "bar", "match_type": "partial"},
#         {"keyword": "brewery", "category_id": "bar", "match_type": "partial"},
        
#         # Google Place types
#         {"keyword": "restaurant", "category_id": "fast_food", "match_type": "type"},
#         {"keyword": "meal_takeaway", "category_id": "fast_food", "match_type": "type"},
#         {"keyword": "meal_delivery", "category_id": "fast_food", "match_type": "type"},
#         {"keyword": "night_club", "category_id": "bar", "match_type": "type"},
#     ]
    
#     get_keywords_col().insert_many(keywords)
#     print(f"✅ Added {len(keywords)} keywords")
    
#     # Insert rules
#     rules = [
#         {
#             "trigger_category_id": "fast_food",
#             "recommended_category_ids": ["healthy_cafe", "smoothie", "walking_trail"],
#             "ai_prompt_template": "User is near fast food. Suggest healthy alternatives."
#         },
#         {
#             "trigger_category_id": "bar",
#             "recommended_category_ids": ["gym", "walking_trail", "smoothie"],
#             "ai_prompt_template": "User is near a bar. Suggest active alternatives."
#         }
#     ]
    
#     get_rules_col().insert_many(rules)
#     print(f"✅ Added {len(rules)} rules")
    
#     print("\n🎉 Database seeding complete!")
#     print(f"📊 Total: {len(categories)} categories, {len(keywords)} keywords, {len(rules)} rules")

# if __name__ == "__main__":
#     seed_database()

# # Add sample menus to the seeding function
# def seed_sample_menus():
#     """Seed sample menu data"""
#     menus_col = get_menus_col() # type: ignore
    
#     sample_menus = [
#         {
#             "place_id": "sample_gym_1",
#             "place_name": "Fitness First Gym",
#             "source": "sample",
#             "items": [
#                 {"name": "Whey Protein Shake", "price": 600, "is_healthy": True, "category": "Supplement"},
#                 {"name": "BCAA Energy Drink", "price": 400, "is_healthy": True, "category": "Supplement"},
#                 {"name": "Grilled Chicken Salad", "price": 800, "is_healthy": True, "category": "Meal"},
#                 {"name": "Energy Bar", "price": 250, "is_healthy": True, "category": "Snack"},
#             ]
#         },
#         {
#             "place_id": "sample_cafe_1",
#             "place_name": "Coffee Planet",
#             "source": "sample",
#             "items": [
#                 {"name": "Cappuccino", "price": 350, "is_healthy": True, "category": "Coffee"},
#                 {"name": "Green Tea", "price": 200, "is_healthy": True, "category": "Tea"},
#                 {"name": "Avocado Toast", "price": 550, "is_healthy": True, "category": "Breakfast"},
#                 {"name": "Fruit Yogurt", "price": 400, "is_healthy": True, "category": "Snack"},
#             ]
#         },
#         {
#             "place_id": "sample_juice_1",
#             "place_name": "Fresh Juice Bar",
#             "source": "sample",
#             "items": [
#                 {"name": "Orange Juice", "price": 300, "is_healthy": True, "category": "Juice"},
#                 {"name": "Carrot Ginger Juice", "price": 350, "is_healthy": True, "category": "Juice"},
#                 {"name": "Mixed Berry Smoothie", "price": 450, "is_healthy": True, "category": "Smoothie"},
#                 {"name": "Protein Smoothie", "price": 500, "is_healthy": True, "category": "Smoothie"},
#             ]   
#         }
#     ]                                                                                                                                                                                                            


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "recommendation_db")]

def seed_complete_database():
    print("🗑️ Clearing old data...")
    db.categories.delete_many({})
    db.keywords.delete_many({})
    db.rules.delete_many({})
    
    print("🌱 Seeding complete database...")
    
    # 1. CATEGORIES (with proper is_unhealthy flag)
    categories = [
        {"_id": "fast_food", "name": "Fast Food", "description": "Fast food restaurants", "is_unhealthy": True},
        {"_id": "bar_pub", "name": "Bar/Pub", "description": "Bars and pubs", "is_unhealthy": True},
        {"_id": "restaurant", "name": "Restaurant", "description": "General restaurants", "is_unhealthy": False},
        {"_id": "cafe", "name": "Cafe", "description": "Coffee shops and cafes", "is_unhealthy": False},
        {"_id": "gym", "name": "Gym/Fitness Center", "description": "Fitness centers", "is_unhealthy": False},
        {"_id": "healthy_cafe", "name": "Healthy Cafe", "description": "Healthy food cafes", "is_unhealthy": False},
        {"_id": "smoothie_shop", "name": "Smoothie Shop", "description": "Smoothie and juice bars", "is_unhealthy": False},
        {"_id": "park", "name": "Park", "description": "Public parks", "is_unhealthy": False},
        {"_id": "walking_trail", "name": "Walking Trail", "description": "Walking paths", "is_unhealthy": False},
    ]
    
    db.categories.insert_many(categories)
    print(f"✅ Added {len(categories)} categories")
    
    # 2. KEYWORDS (for REAL places only)
    keywords = [
        # Fast Food keywords
        {"keyword": "mcdonald", "category_id": "fast_food", "match_type": "partial"},
        {"keyword": "kfc", "category_id": "fast_food", "match_type": "partial"},
        {"keyword": "burger king", "category_id": "fast_food", "match_type": "partial"},
        {"keyword": "pizza hut", "category_id": "fast_food", "match_type": "partial"},
        {"keyword": "subway", "category_id": "fast_food", "match_type": "partial"},
        {"keyword": "domino", "category_id": "fast_food", "match_type": "partial"},
        
        # Bar/Pub keywords
        {"keyword": "bar", "category_id": "bar_pub", "match_type": "partial"},
        {"keyword": "pub", "category_id": "bar_pub", "match_type": "partial"},
        {"keyword": "nightclub", "category_id": "bar_pub", "match_type": "partial"},
        {"keyword": "lounge", "category_id": "bar_pub", "match_type": "partial"},
        {"keyword": "brewery", "category_id": "bar_pub", "match_type": "partial"},
        
        # Cafe keywords
        {"keyword": "cafe", "category_id": "cafe", "match_type": "partial"},
        {"keyword": "coffee", "category_id": "cafe", "match_type": "partial"},
        {"keyword": "starbucks", "category_id": "cafe", "match_type": "partial"},
        
        # Gym keywords
        {"keyword": "gym", "category_id": "gym", "match_type": "partial"},
        {"keyword": "fitness", "category_id": "gym", "match_type": "partial"},
        {"keyword": "workout", "category_id": "gym", "match_type": "partial"},
        
        # Healthy keywords
        {"keyword": "healthy", "category_id": "healthy_cafe", "match_type": "partial"},
        {"keyword": "salad", "category_id": "healthy_cafe", "match_type": "partial"},
        {"keyword": "juice", "category_id": "smoothie_shop", "match_type": "partial"},
        {"keyword": "smoothie", "category_id": "smoothie_shop", "match_type": "partial"},
    ]
    
    db.keywords.insert_many(keywords)
    print(f"✅ Added {len(keywords)} keywords")
    
    # 3. RULES (MOST IMPORTANT!)
    rules = [
        {
            "trigger_category_id": "fast_food",
            "recommended_category_ids": ["healthy_cafe", "smoothie_shop", "park", "gym"],
            "ai_prompt_template": "User is near fast food. Suggest healthy alternatives."
        },
        {
            "trigger_category_id": "bar_pub",
            "recommended_category_ids": ["cafe", "park", "gym", "walking_trail"],
            "ai_prompt_template": "User is near a bar. Suggest active alternatives."
        },
        {
            "trigger_category_id": "gym",
            "recommended_category_ids": ["smoothie_shop", "healthy_cafe", "park"],
            "ai_prompt_template": "User is at a gym. Suggest recovery options."
        },
        {
            "trigger_category_id": "walking_trail",
            "recommended_category_ids": ["healthy_cafe", "smoothie_shop", "park"],
            "ai_prompt_template": "User is on a walking trail. Suggest refuel options."
        },
        {
            "trigger_category_id": "park",
            "recommended_category_ids": ["walking_trail", "gym", "healthy_cafe"],
            "ai_prompt_template": "User is at a park. Suggest additional activities."
        },
    ]
    
    db.rules.insert_many(rules)
    print(f"✅ Added {len(rules)} rules")
    
    print("\n🎉 Database successfully seeded!")
    print("\n📊 Summary:")
    print(f"   Categories: {db.categories.count_documents({})}")
    print(f"   Keywords: {db.keywords.count_documents({})}")
    print(f"   Rules: {db.rules.count_documents({})}")
    print("\n🚀 Now run: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    seed_complete_database()