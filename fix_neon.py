# test_api.py
import requests
import time
import sys

def test_api_endpoints():
    print("🧪 Testing API Endpoints")
    print("="*60)
    
    base_url = "http://localhost:8000"
    
    # Wait for server
    print("Waiting for server to start...")
    time.sleep(2)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/neon-info", "Neon info"),
        ("/api/admin/health", "Admin health"),
        ("/api/admin/categories", "Categories"),
        ("/api/admin/keywords", "Keywords"),
        ("/api/admin/rules", "Rules"),
        ("/api/admin/stats", "Statistics"),
        ("/api/recommend?lat=40.7128&lng=-74.0060", "Recommendations"),
        ("/api/image/analyze-quick?image_url=test", "Image analysis"),
    ]
    
    successful = 0
    total = len(endpoints)
    
    for endpoint, name in endpoints:
        try:
            print(f"\n🔍 Testing: {name}")
            print(f"   GET {base_url}{endpoint}")
            
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {response.status_code}")
                
                # Show relevant info
                if "categories" in data:
                    count = len(data.get("categories", []))
                    print(f"   📁 {count} categories")
                elif "counts" in data:
                    counts = data.get("counts", {})
                    print(f"   📊 Data counts: {counts}")
                elif "database" in data:
                    db = data.get("database", "unknown")
                    print(f"   💾 Database: {db}")
                    
                successful += 1
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Cannot connect to server")
            print(f"   💡 Make sure server is running: python run.py")
            break
        except Exception as e:
            print(f"   ⚠️ Error: {e}")
    
    print("\n" + "="*60)
    print(f"📊 Test Results: {successful}/{total} endpoints successful")
    
    if successful == total:
        print("🎉 All tests passed! Your API is fully functional!")
        print("\n🚀 Next steps:")
        print("   1. Connect your frontend to: http://localhost:8000")
        print("   2. Add your Google Maps and Gemini API keys to .env")
        print("   3. Test with your frontend application")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("="*60)

if __name__ == "__main__":
    test_api_endpoints()