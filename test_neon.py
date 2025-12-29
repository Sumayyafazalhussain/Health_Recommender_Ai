# test_neon.py
print("🔍 Testing Neon PostgreSQL Connection")
print("="*50)

try:
    from app.db.neon_connection import test_connection
    
    # Test connection
    if test_connection():
        print("✅ Connection to Neon successful!")
        
        # Test database operations
        print("\n📊 Testing database operations...")
        
        try:
            from app.services.neon_service import neon_db_service
            
            # Get counts
            health = neon_db_service.health_check()
            print(f"✅ Database health: {health['status']}")
            
            counts = health.get('counts', {})
            print(f"   Categories: {counts.get('categories', 0)}")
            print(f"   Keywords: {counts.get('keywords', 0)}")
            print(f"   Rules: {counts.get('rules', 0)}")
            print(f"   Menus: {counts.get('menus', 0)}")
            
            # Get categories
            print("\n📁 Listing categories:")
            categories = neon_db_service.get_categories()
            for cat in categories[:5]:  # Show first 5
                print(f"   • {cat['name']} (ID: {cat['id']})")
            
            print(f"\n🎉 Neon PostgreSQL is working correctly!")
        except Exception as e:
            print(f"⚠️ Database operations error: {e}")
    else:
        print("❌ Failed to connect to Neon PostgreSQL")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Check your imports and file structure")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*50)