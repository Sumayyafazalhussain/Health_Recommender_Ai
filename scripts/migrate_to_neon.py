# scripts/migrate_to_neon.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from sqlalchemy.orm import Session
import json
from datetime import datetime
import uuid

from app.db.neon_db import get_session_local, Category, Keyword, Rule, Menu, rule_categories
from app.config import settings

def migrate_mongodb_to_neon():
    print("🔄 Migrating MongoDB to Neon PostgreSQL...")
    
    # Connect to MongoDB
    try:
        print("📦 Connecting to MongoDB...")
        mongo_client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
        mongo_db = mongo_client[settings.DB_NAME]
        
        # Test MongoDB connection
        mongo_db.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False
    
    # Initialize Neon database
    print("🔗 Initializing Neon PostgreSQL...")
    from app.db.neon_db import init_db, check_connection
    
    init_db()
    
    if not check_connection():
        print("❌ Cannot connect to Neon PostgreSQL")
        return False
    
    session = get_session_local()()
    
    try:
        # 1. Migrate Categories
        print("📁 Migrating categories...")
        mongo_categories = list(mongo_db.categories.find({}))
        category_map = {}  # Map old MongoDB IDs to new Neon IDs
        
        for cat in mongo_categories:
            mongo_id = str(cat.get('_id', ''))
            neon_id = cat.get('id') or mongo_id or str(uuid.uuid4())
            
            category = Category(
                id=neon_id,
                name=cat.get('name', ''),
                description=cat.get('description'),
                is_unhealthy=cat.get('is_unhealthy', True),
                created_at=cat.get('created_at', datetime.utcnow()),
                updated_at=cat.get('updated_at', datetime.utcnow())
            )
            
            session.add(category)
            category_map[mongo_id] = neon_id
        
        session.commit()
        print(f"✅ Migrated {len(mongo_categories)} categories")
        
        # 2. Migrate Keywords
        print("🔤 Migrating keywords...")
        mongo_keywords = list(mongo_db.keywords.find({}))
        
        for kw in mongo_keywords:
            mongo_category_id = kw.get('category_id')
            neon_category_id = category_map.get(mongo_category_id, mongo_category_id)
            
            keyword = Keyword(
                id=str(kw.get('_id', uuid.uuid4())),
                keyword=kw.get('keyword', ''),
                category_id=neon_category_id,
                match_type=kw.get('match_type', 'partial'),
                created_at=kw.get('created_at', datetime.utcnow())
            )
            session.add(keyword)
        
        session.commit()
        print(f"✅ Migrated {len(mongo_keywords)} keywords")
        
        # 3. Migrate Rules
        print("⚙️ Migrating rules...")
        mongo_rules = list(mongo_db.rules.find({}))
        
        for rule in mongo_rules:
            mongo_trigger_id = rule.get('trigger_category_id')
            neon_trigger_id = category_map.get(mongo_trigger_id, mongo_trigger_id)
            
            db_rule = Rule(
                id=str(rule.get('_id', uuid.uuid4())),
                trigger_category_id=neon_trigger_id,
                ai_prompt_template=rule.get('ai_prompt_template', ''),
                created_at=rule.get('created_at', datetime.utcnow()),
                updated_at=rule.get('updated_at', datetime.utcnow())
            )
            session.add(db_rule)
            session.flush()  # Get rule ID
            
            # Add recommended categories
            recommended_ids = rule.get('recommended_category_ids', [])
            for rec_id in recommended_ids:
                neon_rec_id = category_map.get(rec_id, rec_id)
                # Insert into association table
                session.execute(
                    rule_categories.insert().values(
                        rule_id=db_rule.id,
                        category_id=neon_rec_id
                    )
                )
        
        session.commit()
        print(f"✅ Migrated {len(mongo_rules)} rules")
        
        # 4. Migrate Menus
        print("🍽️ Migrating menus...")
        mongo_menus = list(mongo_db.menus.find({}))
        
        for menu in mongo_menus:
            db_menu = Menu(
                id=str(menu.get('_id', uuid.uuid4())),
                place_id=menu.get('place_id', ''),
                place_name=menu.get('place_name', ''),
                source=menu.get('source', 'google'),
                items=menu.get('items', []),
                last_updated=menu.get('last_updated', datetime.utcnow()),
                created_at=menu.get('created_at', datetime.utcnow())
            )
            session.add(db_menu)
        
        session.commit()
        print(f"✅ Migrated {len(mongo_menus)} menus")
        
        # Show summary
        cat_count = session.query(Category).count()
        kw_count = session.query(Keyword).count()
        rule_count = session.query(Rule).count()
        menu_count = session.query(Menu).count()
        
        print("\n🎉 Migration COMPLETE!")
        print("\n📊 Neon PostgreSQL Summary:")
        print(f"   Categories: {cat_count}")
        print(f"   Keywords: {kw_count}")
        print(f"   Rules: {rule_count}")
        print(f"   Menus: {menu_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        session.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
        mongo_client.close()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("🚀 Starting MongoDB to Neon PostgreSQL Migration")
    print("=" * 50)
    
    success = migrate_mongodb_to_neon()
    
    if success:
        print("\n✅ Migration successful!")
        print("\n💡 Next steps:")
        print("   1. Update your admin routes to use Neon")
        print("   2. Update rule_engine.py to use Neon")
        print("   3. Restart your FastAPI application")
    else:
        print("\n❌ Migration failed")
    
    print("\n🔧 For manual verification:")
    print("   - Go to Neon Dashboard: https://console.neon.tech")
    print("   - Check your project's tables")