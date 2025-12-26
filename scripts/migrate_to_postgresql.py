"""
Script to migrate data from MongoDB to PostgreSQL
Run with: python scripts/migrate_to_postgresql.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import uuid

from app.db.database__adapter import get_engine, Category, Keyword, Rule, Menu
from sqlalchemy.orm import sessionmaker

load_dotenv()

def migrate_mongodb_to_postgresql():
    print("🔄 Starting MongoDB to PostgreSQL migration...")
    print("=" * 50)
    
    # Initialize PostgreSQL database
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    pg_session = SessionLocal()
    
    # Connect to MongoDB
    try:
        mongo_client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        db = mongo_client[os.getenv("DB_NAME", "recommendation_db")]
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return
    
    try:
        print("🗑️ Clearing existing PostgreSQL data...")
        pg_session.query(Keyword).delete()
        # Clear association table using raw SQL
        pg_session.execute("DELETE FROM rule_categories")
        pg_session.query(Rule).delete()
        pg_session.query(Category).delete()
        pg_session.query(Menu).delete()
        pg_session.commit()
        print("✅ PostgreSQL tables cleared")
        
        # 1. Migrate Categories
        print("\n📁 Migrating categories...")
        mongo_categories = list(db.categories.find({}))
        categories_map = {}  # Store mapping of old_id -> new_category
        
        for mongo_cat in mongo_categories:
            # Convert ObjectId to string if needed
            if hasattr(mongo_cat['_id'], '__str__'):
                cat_id = str(mongo_cat['_id'])
            else:
                cat_id = mongo_cat['_id']
            
            category = Category(
                id=cat_id,
                name=mongo_cat.get('name', 'Unnamed Category'),
                description=mongo_cat.get('description'),
                is_unhealthy=mongo_cat.get('is_unhealthy', True),
                created_at=mongo_cat.get('created_at', datetime.utcnow()),
                updated_at=mongo_cat.get('updated_at', datetime.utcnow())
            )
            pg_session.add(category)
            categories_map[cat_id] = category
        
        pg_session.commit()
        print(f"✅ Migrated {len(mongo_categories)} categories")
        
        # 2. Migrate Keywords
        print("\n🔤 Migrating keywords...")
        mongo_keywords = list(db.keywords.find({}))
        
        for mongo_kw in mongo_keywords:
            # Convert ObjectId to string if needed
            if hasattr(mongo_kw['_id'], '__str__'):
                kw_id = str(mongo_kw['_id'])
            else:
                kw_id = mongo_kw['_id']
            
            # Check if category exists
            category_id = mongo_kw.get('category_id')
            if category_id not in categories_map:
                print(f"⚠️ Skipping keyword - category {category_id} not found")
                continue
            
            keyword = Keyword(
                id=kw_id,
                keyword=mongo_kw.get('keyword', ''),
                category_id=category_id,
                match_type=mongo_kw.get('match_type', 'partial'),
                created_at=mongo_kw.get('created_at', datetime.utcnow())
            )
            pg_session.add(keyword)
        
        pg_session.commit()
        print(f"✅ Migrated {len(mongo_keywords)} keywords")
        
        # 3. Migrate Rules
        print("\n⚙️ Migrating rules...")
        mongo_rules = list(db.rules.find({}))
        
        for mongo_rule in mongo_rules:
            # Convert ObjectId to string if needed
            if hasattr(mongo_rule['_id'], '__str__'):
                rule_id = str(mongo_rule['_id'])
            else:
                rule_id = mongo_rule['_id']
            
            # Check trigger category exists
            trigger_cat_id = mongo_rule.get('trigger_category_id')
            if trigger_cat_id not in categories_map:
                print(f"⚠️ Skipping rule - trigger category {trigger_cat_id} not found")
                continue
            
            rule = Rule(
                id=rule_id,
                trigger_category_id=trigger_cat_id,
                ai_prompt_template=mongo_rule.get('ai_prompt_template', 
                    "User is near a {trigger_category}. Suggest healthy alternatives like {alternatives}."),
                created_at=mongo_rule.get('created_at', datetime.utcnow()),
                updated_at=mongo_rule.get('updated_at', datetime.utcnow())
            )
            
            # Add recommended categories
            recommended_ids = mongo_rule.get('recommended_category_ids', [])
            for rec_id in recommended_ids:
                if rec_id in categories_map:
                    rule.recommended_categories.append(categories_map[rec_id])
                else:
                    print(f"⚠️ Skipping recommended category {rec_id} - not found")
            
            pg_session.add(rule)
        
        pg_session.commit()
        print(f"✅ Migrated {len(mongo_rules)} rules")
        
        # 4. Migrate Menus
        print("\n🍽️ Migrating menus...")
        mongo_menus = list(db.menus.find({}))
        
        for mongo_menu in mongo_menus:
            # Convert ObjectId to string if needed
            if hasattr(mongo_menu['_id'], '__str__'):
                menu_id = str(mongo_menu['_id'])
            else:
                menu_id = mongo_menu['_id']
            
            menu = Menu(
                id=menu_id,
                place_id=mongo_menu.get('place_id', ''),
                place_name=mongo_menu.get('place_name', ''),
                items=mongo_menu.get('items', []),
                source=mongo_menu.get('source', 'google'),
                last_updated=mongo_menu.get('last_updated', datetime.utcnow()),
                created_at=mongo_menu.get('created_at', datetime.utcnow())
            )
            pg_session.add(menu)
        
        pg_session.commit()
        print(f"✅ Migrated {len(mongo_menus)} menus")
        
        print("\n" + "=" * 50)
        print("🎉 Migration completed successfully!")
        print("\n📊 PostgreSQL Database Summary:")
        print(f"   Categories: {pg_session.query(Category).count()}")
        print(f"   Keywords: {pg_session.query(Keyword).count()}")
        print(f"   Rules: {pg_session.query(Rule).count()}")
        print(f"   Menus: {pg_session.query(Menu).count()}")
        print("\n✅ You can now use PostgreSQL as your database!")
        
    except Exception as e:
        pg_session.rollback()
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        pg_session.close()
        if 'mongo_client' in locals():
            mongo_client.close()

if __name__ == "__main__":
    migrate_mongodb_to_postgresql()