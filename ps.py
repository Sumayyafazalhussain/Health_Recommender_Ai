# test_final.py
import requests
import time
import sys

def test_all_endpoints():
    print("🧪 FINAL TEST - Neon PostgreSQL Backend")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    # Wait for server
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    endpoints = [
        ("GET", "/", "Root"),
        ("GET", "/health", "Health Check"),
        ("GET", "/admin/health", "Admin Health"),
        ("GET", "/admin/categories", "Categories"),
        ("GET", "/admin/keywords", "Keywords"),
        ("GET", "/admin/rules", "Rules"),
        ("GET", "/admin/stats", "Statistics"),
        ("GET", "/admin/test-neon", "Neon Test"),
        ("GET", "/api/neon/info", "Neon Info"),
        ("GET", "/api/neon/check", "Neon Check"),
    ]
    
    passed = 0
    failed = 0
    
    for method, endpoint, name in endpoints:
        try:
            print(f"\n🔍 Testing: {name}")
            print(f"   {method} {base_url}{endpoint}")
            
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: 200")
                
                # Show relevant info
                if "categories" in data:
                    count = len(data.get("categories", []))
                    print(f"   📁 Categories: {count}")
                elif "keywords" in data:
                    count = len(data.get("keywords", []))
                    print(f"   🔤 Keywords: {count}")
                elif "rules" in data:
                    count = len(data.get("rules", []))
                    print(f"   ⚙️ Rules: {count}")
                elif "counts" in data:
                    counts = data.get("counts", {})
                    print(f"   📊 Data counts: {counts}")
                elif "database" in data:
                    db = data.get("database", "unknown")
                    print(f"   💾 Database: {db}")
                
                passed += 1
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text[:100]}...")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Cannot connect to server")
            print(f"   💡 Start server with: python run.py")
            failed += 1
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    
    if passed >= 8:
        print("🎉 SUCCESS! Your Neon PostgreSQL backend is working!")
        print("\n🚀 Next steps:")
        print("   1. Your frontend should connect to: http://localhost:8000")
        print("   2. Check Neon Dashboard: https://console.neon.tech")
        print("   3. Test with your actual frontend application")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("="*60)
    
    return passed > failed

if __name__ == "__main__":
    success = test_all_endpoints()
    sys.exit(0 if success else 1)