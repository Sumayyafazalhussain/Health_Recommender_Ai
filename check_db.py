"""
Quick PostgreSQL database check
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database():
    print("🔍 Checking Database Configuration...")
    print("="*50)
    
    try:
        from app.config import settings
        print(f"✅ Config loaded")
        print(f"   Database Type: {settings.DATABASE_TYPE}")
        print(f"   PostgreSQL URL: {settings.POSTGRES_URL}")
        
        if settings.DATABASE_TYPE == "postgresql":
            print("\n🔄 Testing PostgreSQL connection...")
            from sqlalchemy import create_engine, text
            
            try:
                engine = create_engine(settings.POSTGRES_URL)
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"✅ Connected to PostgreSQL!")
                    print(f"   Version: {version}")
                    
                    # Check database
                    result = conn.execute(text("SELECT current_database()"))
                    db_name = result.fetchone()[0]
                    print(f"   Database: {db_name}")
                    
                    # Check tables
                    result = conn.execute(text("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """))
                    tables = [row[0] for row in result.fetchall()]
                    
                    if tables:
                        print(f"✅ Found {len(tables)} tables")
                        for table in tables:
                            print(f"   - {table}")
                    else:
                        print("ℹ️ No tables found. Will create them on startup.")
                
                return True
            except Exception as e:
                print(f"❌ PostgreSQL connection failed: {e}")
                print("\n🔧 Troubleshooting:")
                print("1. Check if PostgreSQL is running")
                print("2. Check .env file:")
                print(f"   POSTGRES_URL={settings.POSTGRES_URL}")
                print("3. Test connection in pgAdmin")
                return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if check_database():
        print("\n✅ Database check passed!")
        print("\n🚀 You can now run: python run.py")
    else:
        print("\n❌ Database check failed!")
        print("\n📋 Next steps:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Create database 'health_recommender' in pgAdmin")
        print("3. Update .env file with correct credentials")